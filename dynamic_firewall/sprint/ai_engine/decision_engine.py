import json

with open("ai_engine/attack_knowledge.json") as f:
    knowledge = json.load(f)

def decide(attack_type, confidence):
    if attack_type in knowledge["known_attacks"]:
        return "AI_BLOCK"
    else:
        if confidence > 0.7:
            return "ESCALATE_TO_CONTROLLER"
        else:
            return "MONITOR"

