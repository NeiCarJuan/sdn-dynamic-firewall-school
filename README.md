# SDN-based Dynamic Firewall for School Network

## Overview
This project implements a SDN-based dynamic firewall using OpenFlow and Ryu,
integrated with a simple AI (z-score) and Captive Portal to protect school networks.

## Architecture
- SDN Controller: Ryu (OpenFlow)
- Data Plane: Mininet + Open vSwitch
- AI: Statistical anomaly detection (z-score) with adaptive learning
- Captive Portal & Dashboard: Flask Web App

## Team
- Ninh: SDN Controller, Firewall, AI, Network Simulation
- Biên: Captive Portal, Dashboard, Web Integration

## Repository Structure
- controller/: SDN firewall & AI (Ubuntu VM)
- portal/: Captive Portal & Dashboard (Web)
- docs/: Report, diagrams, slides
