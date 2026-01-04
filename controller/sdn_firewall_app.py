from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet, ethernet, ipv4
import logging
import os

# =========================
# Sprint 3 configuration
# =========================
ACCOUNTING_IP = "10.0.0.2"
ATTACKER_IP = "10.0.0.100"
LOG_FILE = "controller/logs/accounting.log"

os.makedirs("controller/logs", exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# =========================
# SDN Firewall Application
# =========================
class SDNFirewall(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(SDNFirewall, self).__init__(*args, **kwargs)
        self.mac_to_port = {}
        self.logger.info("SDN Firewall (Sprint 3) started")

    # -------------------------
    # Install default rule
    # -------------------------
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [
            parser.OFPActionOutput(
                ofproto.OFPP_CONTROLLER,
                ofproto.OFPCML_NO_BUFFER
            )
        ]
        inst = [
            parser.OFPInstructionActions(
                ofproto.OFPIT_APPLY_ACTIONS,
                actions
            )
        ]

        mod = parser.OFPFlowMod(
            datapath=datapath,
            priority=0,
            match=match,
            instructions=inst
        )
        datapath.send_msg(mod)
        self.logger.info("Default flow installed (send to controller)")

    # -------------------------
    # Packet processing
    # -------------------------
    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        dpid = datapath.id

        self.mac_to_port.setdefault(dpid, {})

        pkt = packet.Packet(msg.data)
        eth = pkt.get_protocol(ethernet.ethernet)

        # Ignore LLDP
        if eth.ethertype == 0x88cc:
            return

        src_mac = eth.src
        dst_mac = eth.dst
        in_port = msg.match['in_port']

        self.mac_to_port[dpid][src_mac] = in_port

        # IP layer
        ip_pkt = pkt.get_protocol(ipv4.ipv4)
        if ip_pkt:
            src_ip = ip_pkt.src
            dst_ip = ip_pkt.dst

            # 🔒 BLOCK attacker → accounting
            if src_ip == ATTACKER_IP and dst_ip == ACCOUNTING_IP:
                logging.warning(
                    f"BLOCKED ATTACKER: {src_ip} -> {dst_ip}"
                )
                return

            # 🔒 BLOCK non-accounting → accounting
            if dst_ip == ACCOUNTING_IP and src_ip != ACCOUNTING_IP:
                logging.warning(
                    f"BLOCKED UNAUTHORIZED: {src_ip} -> {dst_ip}"
                )
                return

        # Learning switch logic
        if dst_mac in self.mac_to_port[dpid]:
            out_port = self.mac_to_port[dpid][dst_mac]
        else:
            out_port = ofproto.OFPP_FLOOD

        actions = [parser.OFPActionOutput(out_port)]

        # Install flow for known destination
        if out_port != ofproto.OFPP_FLOOD:
            match = parser.OFPMatch(
                in_port=in_port,
                eth_dst=dst_mac
            )
            mod = parser.OFPFlowMod(
                datapath=datapath,
                priority=1,
                match=match,
                instructions=[
                    parser.OFPInstructionActions(
                        ofproto.OFPIT_APPLY_ACTIONS,
                        actions
                    )
                ]
            )
            datapath.send_msg(mod)

        # Send packet
        out = parser.OFPPacketOut(
            datapath=datapath,
            buffer_id=msg.buffer_id,
            in_port=in_port,
            actions=actions,
            data=msg.data
        )
        datapath.send_msg(out)

        self.logger.info(
            f"FORWARD: {src_mac} -> {dst_mac} (dpid={dpid})"
        )
