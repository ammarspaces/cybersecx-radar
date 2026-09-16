#!/usr/bin/env python3

import argparse
import json
import random
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================
# CONFIG
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

RESOURCE_FILE = BASE_DIR / "resources.json"
HISTORY_FILE = BASE_DIR / "picker_history.json"

HISTORY_LIMIT = 100



# ============================================================
# TYPE INSTRUCTIONS
# ============================================================

TYPE_INSTRUCTIONS = {

    "social":
        "Treat this as a SENSOR. Find signals, not conclusions.",

    "professional":
        "Treat this as a professional ecosystem sensor.",

    "community":
        "Treat this as CONTEXT. Community discussion is not automatically evidence.",

    "news":
        "Treat this as DISCOVERY. Trace interesting claims to primary material.",

    "technical_news":
        "Use the article as a lead, then locate the technical source.",

    "database":
        "Use this for VERIFICATION. Check metadata and cross-reference.",

    "exploitation_database":
        "Determine whether exploitation is real, theoretical, or historical.",

    "malware_database":
        "Inspect the artifact metadata before drawing conclusions.",

    "ioc_database":
        "Pivot from IOC → infrastructure → malware/campaign.",

    "sandbox":
        "Observe behavior first. Build hypotheses from telemetry.",

    "threat_intelligence":
        "Build relationships between indicators, actors, campaigns and infrastructure.",

    "threat_research":
        "Reconstruct the attack chain and identify TTPs.",

    "malware_research":
        "Focus on behavior, artifacts, and technical mechanism.",

    "reverse_engineering":
        "Focus on understanding how the artifact works.",

    "offensive_research":
        "Understand the vulnerability/root cause rather than merely the exploit.",

    "framework":
        "Use the framework to structure an investigation.",

    "detection":
        "Ask: what behavior is this detecting and what telemetry is required?",

    "adversary_emulation":
        "Use a safe lab and compare expected vs observed telemetry.",

    "case_study":
        "Reconstruct the incident chronologically.",

    "dfir_tool":
        "Start with the evidence/artifact and work toward the hypothesis.",

    "memory_forensics":
        "Identify what artifact the plugin extracts and why it matters.",

    "network_security":
        "Think in terms of traffic, protocol, behavior and telemetry.",

    "pcap_analysis":
        "Start with the packet evidence, not assumptions.",

    "ids":
        "Understand the traffic pattern behind the signature.",

    "internet_measurement":
        "Understand the dataset and measurement methodology.",

    "web_observation":
        "Pivot from URL → DNS → HTTP → infrastructure.",

    "reverse_engineering_tool":
        "Use a small safe artifact and document your observations.",

    "dynamic_instrumentation":
        "Observe runtime behavior through controlled instrumentation.",

    "binary_analysis":
        "Understand the program behavior rather than blindly following a recipe.",

    "debugger":
        "Form a hypothesis, then verify it with runtime behavior.",

    "lab":
        "Attempt first. Read the solution only when genuinely stuck.",

    "dfir_lab":
        "Treat the challenge as an investigation, not a quiz.",

    "blue_team_lab":
        "Think like an analyst: evidence → hypothesis → conclusion.",

    "soc_lab":
        "Treat the alert as a real investigation.",

    "web_lab":
        "Understand the vulnerability mechanism, not merely the payload.",

    "academic":
        "Extract problem → methodology → result → limitation.",

    "conference_research":
        "Treat the paper/talk as technical research, not entertainment.",

    "privacy_research":
        "Identify threat model, privacy property and methodology.",

    "conference":
        "Pick ONE talk. Don't consume the entire conference.",

    "conference_aggregator":
        "Use this to discover people, conferences and research topics.",

    "ctf":
        "Solve first. Read writeups later.",

    "ctf_aggregator":
        "Use it as a discovery mechanism for practical experiments.",

    "investigation":
        "Document the evidence chain.",

    "investigation_tool":
        "Validate interesting results manually.",

    "reference":
        "Use it as a map, then verify important claims elsewhere.",

    "mailing_list":
        "Look for the original technical discussion or patch.",

    "fuzzing":
        "Focus on the bug class and how the fuzzer discovered it.",

    "mobile_analysis":
        "Analyze only applications you are authorized to test.",

    "mobile_lab":
        "Use a controlled test application.",

    "platform_security":
        "Understand the platform security boundary.",

    "vulnerability_advisory":
        "Identify affected component, root cause and remediation.",

    "vulnerability_research":
        "Trace the vulnerability to root cause and impact.",

    "security_advisory":
        "Determine affected versions and remediation.",

    "open_source_security":
        "Trace the issue to the patch/commit.",

    "magazine":
        "ONE ARTICLE ONLY. The goal is discovery and deep curiosity, not finishing the publication.",

    "technical_creator":
        "Treat the creator as a lead generator. Verify important claims independently.",

    "training":
        "Learn one concept and immediately test it.",

    "identity_security":
        "Think in terms of identity, privileges, attack paths and detection.",

    "government_security":
        "Treat the publication as an operational signal and verify technical details.",

    "regulatory":
        "Focus on implications and underlying technical issues.",

    "technology_ecosystem":
        "Use this to understand regional cybersecurity ecosystem signals.",

    "technology":
        "Identify the technology/security relationship.",

    "cloud_security":
        "Map the cloud attack surface and trust boundaries.",

    "ot_security":
        "Focus on the industrial system, protocol and operational impact.",

    "ot_research":
        "Understand the industrial attack surface and safety implications.",

    "security_tooling":
        "Understand the problem the tool solves before using it.",

    "scanner":
        "Only scan systems you are authorized to test.",

    "bug_bounty":
        "Study public disclosures and use authorized targets only.",

    "security":
        "Separate security claims from marketing claims.",

    "research":
        "Extract the research question, methodology and evidence.",

    "academic_search":
        "Use this to build a citation trail.",

    "bibliography":
        "Use this to discover researchers and research clusters.",

    "repository":
        "Inspect the code, README, issues, commits and release history.",

    "repository_security":
        "Look for code, advisories, commits and PoCs.",

    "technical_blog":
        "Treat the article as a lead and verify important claims.",

    "security_news":
        "Find the technical source behind the story.",

    "open_source":
        "Trace interesting changes to commits and patches.",

    "government_technology":
        "Look for technology/security initiatives and their implications.",

    "security_education":
        "Find one technique worth learning.",

    "technology_ecosystem":
        "Use this as regional ecosystem discovery.",

    "regulatory":
        "Identify the technical implications of policy/regulation.",

    "internet_intelligence":
        "Treat the IP as a starting point for investigation.",

    "network_intelligence":
        "Look for current network signals and validate them.",

    "technical_research":
        "Understand the technical mechanism and evidence.",

    "vulnerability_database":
        "Cross-reference the vulnerability with other databases.",

    "malware_archive":
        "Use samples as artifacts for controlled analysis.",

    "malware_re":
        "Focus on behavior, artifacts and implementation.",

    "conference_video":
        "Pick one talk and extract one technical concept.",

    "technical_research":
        "Identify the research question and technical contribution.",
}


# ============================================================
# FILE MANAGEMENT
# ============================================================

def save_json(path, data):
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def load_json(path, default):
    if not path.exists():
        return default

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[!] Could not read {path.name}: {exc}")
        print("[!] Using default data.")
        return default


def load_resources():
    global CORE_LOOP_FIELDS, DEEP_INVESTIGATION_FIELDS

    if not RESOURCE_FILE.exists():
        print("[!] resources.json not found.")
        print("[!] Please create resources.json first.")
        raise SystemExit(1)

    data = load_json(
        RESOURCE_FILE,
        None
    )

    if data is None:
        raise SystemExit(1)

    if isinstance(data, dict):
        resources = data.get("resources")

        if not isinstance(resources, list):
            print("[!] Invalid resources.json: 'resources' must be a list.")
            raise SystemExit(1)

    if isinstance(data, list):
        resources = data
        CORE_LOOP_FIELDS = []
        DEEP_INVESTIGATION_FIELDS = set()
        return resources

    if not isinstance(data, dict):
        print("[!] Invalid resources.json format.")
        raise SystemExit(1)

    radar = data.get("radar", {})
    core_loop = radar.get("core_loop", [])
    deep_schema = data.get("deep_investigation_schema", {})
    deep_fields = deep_schema.get("required_fields", [])

    if not isinstance(core_loop, list) or not all(isinstance(x, str) and x for x in core_loop):
        print("[!] Invalid radar.core_loop contract in resources.json.")
        raise SystemExit(1)
    if not isinstance(deep_fields, list) or not all(isinstance(x, str) and x for x in deep_fields):
        print("[!] Invalid deep_investigation_schema contract in resources.json.")
        raise SystemExit(1)

    CORE_LOOP_FIELDS = list(core_loop)
    DEEP_INVESTIGATION_FIELDS = set(deep_fields)

    schema_fields = set(data.get("schema", {}).get("resource", {}))
    if not schema_fields:
        print("[!] resources.json is missing schema.resource.")
        raise SystemExit(1)

    required_resource_fields = {
        "id", "name", "domain", "path", "type", "categories",
        "regions", "tier", "role", "tags", "health"
    }
    if not required_resource_fields.issubset(schema_fields):
        print("[!] schema.resource is missing required fields.")
        raise SystemExit(1)

    ids = set()
    for index, resource in enumerate(resources, 1):
        if not isinstance(resource, dict):
            print(f"[!] Invalid resource at index {index}: expected object.")
            raise SystemExit(1)
        missing = required_resource_fields - set(resource)
        if missing:
            print(f"[!] Resource {index} is missing fields: {sorted(missing)}")
            raise SystemExit(1)
        rid = resource.get("id")
        if not isinstance(rid, str) or not rid.strip() or rid in ids:
            print(f"[!] Invalid or duplicate resource id at index {index}: {rid!r}")
            raise SystemExit(1)
        ids.add(rid)
        if not isinstance(resource["categories"], list) or not isinstance(resource["regions"], list):
            print(f"[!] Resource {rid} has invalid categories/regions type.")
            raise SystemExit(1)
        if not isinstance(resource["role"], list) or not isinstance(resource["tags"], list):
            print(f"[!] Resource {rid} has invalid role/tags type.")
            raise SystemExit(1)
        if not isinstance(resource["health"], dict):
            print(f"[!] Resource {rid} has invalid health type.")
            raise SystemExit(1)

    return resources


NORMAL_HISTORY_REQUIRED = {
    "timestamp",
    "resource_id",
    "resource",
    "categories",
    "regions",
    "type",
    "tier",
    "mission",
    "mode",
}

WEEKLY_HISTORY_REQUIRED = {
    "timestamp",
    "mode",
    "week",
    "interesting_signals",
    "sources",
    "evidence",
    "hands_on",
    "result",
    "artifact",
    "publish",
}

DEEP_INVESTIGATION_FIELDS = set()
CORE_LOOP_FIELDS = []
HISTORY_WRITE_ENABLED = True


def validate_history_entry(item):
    if not isinstance(item, dict):
        return False

    mode = item.get("mode")

    if mode == "weekly_summary":
        if not WEEKLY_HISTORY_REQUIRED.issubset(item):
            return False
        return (
            isinstance(item.get("interesting_signals"), list)
            and isinstance(item.get("sources"), list)
            and isinstance(item.get("evidence"), list)
            and isinstance(item.get("hands_on"), list)
            and isinstance(item.get("publish"), bool)
        )

    if not NORMAL_HISTORY_REQUIRED.issubset(item):
        return False

    if not isinstance(item.get("categories"), list):
        return False
    if not isinstance(item.get("regions"), list):
        return False

    investigation = item.get("investigation")
    if investigation is not None:
        if not isinstance(investigation, dict):
            return False
        if set(investigation) != DEEP_INVESTIGATION_FIELDS:
            return False

    return True


def load_history():
    global HISTORY_WRITE_ENABLED
    HISTORY_WRITE_ENABLED = True

    if not HISTORY_FILE.exists():
        return []

    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except Exception as exc:
        HISTORY_WRITE_ENABLED = False
        print(f"[!] Could not read {HISTORY_FILE.name}: {exc}")
        print("[!] History file was not overwritten. Starting with empty in-memory history.")
        return []

    if not isinstance(data, list):
        HISTORY_WRITE_ENABLED = False
        print("[!] Invalid picker_history.json: history must be a list.")
        print("[!] History file was not overwritten. Starting with empty in-memory history.")
        return []

    valid = []
    invalid_count = 0

    for item in data:
        if validate_history_entry(item):
            valid.append(item)
        else:
            invalid_count += 1

    if invalid_count:
        print(f"[!] Ignored {invalid_count} malformed history entr{'y' if invalid_count == 1 else 'ies'}." )

    return valid[-HISTORY_LIMIT:]


# ============================================================
# RANDOMIZATION ENGINE
# ============================================================

def recent_history(history, hours=24):
    cutoff = datetime.now() - timedelta(hours=hours)

    result = []

    for item in history:
        try:
            timestamp = datetime.fromisoformat(item["timestamp"])

            if timestamp >= cutoff:
                result.append(item)

        except Exception:
            continue

    return result


def choose_category(resources, history):
    categories = sorted({
        category
        for resource in resources
        for category in resource.get("categories", [])
    })

    if not categories:
        raise ValueError("No resource categories found.")

    recent = recent_history(history, 24)

    recent_categories = {
        category
        for item in recent
        for category in item.get("categories", [])
    }

    available = [
        category
        for category in categories
        if category not in recent_categories
    ]

    if not available:
        available = categories

    return random.choice(available)


def choose_resource(resources, category, history):
    candidates = [
        resource
        for resource in resources
        if category in resource.get("categories", [])
    ]

    if not candidates:
        raise ValueError(
            f"No resources found for category: {category}"
        )

    recent = recent_history(history, 24)

    recent_resources = {
        item.get("resource_id")
        for item in recent
    }

    fresh = [
        resource
        for resource in candidates
        if resource.get("id") not in recent_resources
    ]

    if fresh:
        candidates = fresh

    return random.choice(candidates)


def choose_mission(resource):
    resource_type = resource.get("type", "reference")

    missions = {
        "signal": [
            "Find one interesting signal from this resource.",
            "Identify one security event or development worth investigating.",
            "Look for something unusual, emerging, or technically interesting.",
        ],
        "research": [
            "Find one research topic and identify the primary technical source.",
            "Extract the research question, methodology, and key finding.",
            "Identify one technical claim worth validating.",
        ],
        "vulnerability": [
            "Find one interesting vulnerability and trace it to its primary advisory.",
            "Identify the affected component, root cause, impact, and remediation.",
            "Determine whether exploitation is real, theoretical, or historical.",
        ],
        "malware": [
            "Find one malware artifact or campaign worth investigating.",
            "Trace an interesting IOC toward the malware, campaign, or infrastructure behind it.",
            "Identify one behavioral characteristic and determine how it could be detected.",
        ],
        "network": [
            "Find one interesting network signal and investigate the underlying traffic behavior.",
            "Identify one network behavior worth reproducing or analyzing.",
            "Find a useful PCAP, telemetry source, or network observation and investigate it.",
        ],
        "detection": [
            "Find one detection rule and determine what behavior and telemetry it relies on.",
            "Identify one ATT&CK technique and investigate how it could be detected.",
            "Find one detection opportunity and turn it into a small detection experiment.",
        ],
        "lab": [
            "Attempt one practical challenge without reading the solution first.",
            "Investigate one scenario and document the evidence chain.",
            "Complete one focused hands-on exercise and record what you learned.",
        ],
        "conference": [
            "Pick ONE talk and extract one technical concept worth investigating.",
            "Find one talk that raises a technical question you want to explore.",
        ],
        "academic": [
            "Pick ONE paper and extract its problem, methodology, result, and limitation.",
            "Find one research claim worth reproducing or testing.",
        ],
        "magazine": [
            "Read ONE article only. Follow the most interesting technical lead.",
            "Pick ONE article and identify one topic worth investigating further.",
        ],
    }

    type_to_mission_group = {
        # Signal / discovery
        "social": "signal",
        "community_platform": "signal",
        "technical_community": "signal",
        "reddit": "signal",
        "fediverse": "signal",
        "news": "signal",
        "security_digest": "signal",
        "event_directory": "signal",
        "blue_team_lab": "lab",
        "conference_directory": "signal",
        "conference_network": "signal",
        "technology_ecosystem": "signal",
        "security_ecosystem": "signal",
        "government_security": "signal",
        "government_technology": "signal",
        "cert": "signal",
        "cert_community": "signal",
        "government_cert": "signal",
        "national_cert": "signal",
        "video_platform": "signal",
        "video_channel": "conference",

        # Vulnerability / disclosure / exploitation
        "advisory_database": "vulnerability",
        "vulnerability_database": "vulnerability",
        "security_advisory": "vulnerability",
        "vulnerability_research": "vulnerability",
        "vulnerability_community": "vulnerability",
        "vulnerability_program": "vulnerability",
        "exploit_database": "vulnerability",
        "bug_bounty_platform": "vulnerability",
        "mobile_security_company": "vulnerability",

        # Malware / IOC / analysis
        "botnet_tracker": "malware",
        "ioc_database": "malware",
        "malware_analysis": "malware",
        "malware_archive": "malware",
        "malware_knowledgebase": "malware",
        "malware_repository": "malware",
        "sandbox": "malware",
        "url_repository": "malware",
        "url_analysis": "malware",
        "threat_intel": "malware",
        "threat_intel_platform": "malware",

        # Research / primary technical material
        "academic_index": "academic",
        "academic_organization": "academic",
        "academic_platform": "academic",
        "academic_repository": "academic",
        "academic_research": "academic",
        "academic_search": "academic",
        "academic_security": "academic",
        "ai_security": "research",
        "ai_security_company": "research",
        "ai_security_framework": "research",
        "ai_security_research": "research",
        "code_platform": "research",
        "cryptographic_library": "research",
        "cryptography_organization": "academic",
        "incident_report": "research",
        "knowledgebase": "research",
        "mailing_list": "research",
        "open_source_project": "research",
        "research_company": "research",
        "research_team": "research",
        "researcher_network": "research",
        "osint_research": "research",
        "security_company": "research",
        "security_company_research": "research",
        "security_documentation": "research",
        "security_organization": "research",
        "security_research": "research",
        "security_community": "research",
        "threat_intel": "malware",
        "ot_security_company": "research",
        "mobile_security_company": "vulnerability",

        # Network / infrastructure observation
        "network_analysis": "network",
        "network_security": "network",
        "network_security_tool": "network",
        "ids": "network",
        "internet_measurement": "network",
        "internet_observation": "network",
        "internet_registry": "network",
        "dns_osint": "network",

        # Detection / adversary emulation
        "detection_database": "detection",
        "detection_framework": "detection",
        "detection_platform": "detection",
        "adversary_simulation": "detection",
        "security_framework": "detection",
        "ai_security_framework": "detection",

        # Hands-on / labs / tooling
        "binary_analysis_framework": "lab",
        "ctf": "lab",
        "ctf_directory": "signal",
        "ctf_platform": "lab",
        "debugger": "lab",
        "dfir_lab_platform": "lab",
        "dfir_tool": "lab",
        "dynamic_instrumentation": "lab",
        "fuzzing_project": "lab",
        "lab_platform": "lab",
        "malware_knowledgebase": "malware",
        "mobile_security_platform": "lab",
        "mobile_security_tool": "lab",
        "osint_platform": "lab",
        "osint_tool": "lab",
        "osint_toolkit": "lab",
        "reverse_engineering_community": "research",
        "reverse_engineering_tool": "lab",
        "security_academy": "lab",
        "security_lab": "lab",
        "security_education": "lab",
        "security_platform": "lab",
        "security_tooling": "lab",
        "soc_lab_platform": "lab",
        "vulnerability_scanner": "lab",

        # Conferences / talks
        "conference": "conference",
    }

    group = type_to_mission_group.get(
        resource_type,
        "research"
    )

    return random.choice(missions[group])


# ============================================================
# HISTORY
# ============================================================

def save_history(history):
    if not HISTORY_WRITE_ENABLED:
        print("[!] History persistence is disabled because picker_history.json could not be safely loaded.")
        print("[!] No history changes were written.")
        return False
    save_json(HISTORY_FILE, history)
    return True


def add_history(history, resource, mission, mode, investigation=None):
    entry = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "resource_id": resource.get("id"),
        "resource": resource.get("name"),
        "categories": resource.get("categories", []),
        "regions": resource.get("regions", []),
        "type": resource.get("type"),
        "tier": resource.get("tier"),
        "mission": mission,
        "mode": mode,
        "record_type": "pick",
    }

    if investigation is not None:
        entry["investigation"] = investigation

    history.append(entry)

    if len(history) > HISTORY_LIMIT:
        del history[:-HISTORY_LIMIT]

    save_history(history)

    return history


# ============================================================
# DISPLAY
# ============================================================

def display_pick(resource, mission, mode):
    instruction = TYPE_INSTRUCTIONS.get(
        resource.get("type"),
        "Treat this as a discovery source."
    )

    print()
    print("=" * 68)
    print("                 🛰️ CYBERSECURITY RADAR")
    print("=" * 68)

    print()
    print("🎲 RANDOM PICK")
    print()

    print(f"Mode     : {mode}")
    print(f"Type     : {resource.get('type', '?')}")
    print(f"Tier     : {resource.get('tier', '?')}")

    categories = resource.get("categories", [])
    if categories:
        print(f"Categories: {', '.join(categories)}")
    else:
        print("Categories: -")

    regions = resource.get("regions", [])
    if regions:
        print(f"Regions  : {', '.join(regions)}")
    else:
        print("Regions  : -")

    print()
    print(f"Resource : {resource.get('name', '?')}")

    domain = resource.get("domain")
    path = resource.get("path", "")

    if domain:
        scheme = resource.get("scheme", "https")
        url = f"{scheme}://{domain}{path}"
        print(f"Link     : {url}")
    else:
        print("Link     : Search manually")

    print()
    print("MISSION")
    print("-" * 68)
    print(mission)

    print()
    print("HOW TO APPROACH")
    print("-" * 68)
    print(instruction)

    print()
    print("ANTI-COLLECTOR")
    print("-" * 68)
    print("Don't bookmark everything.")
    print("If it is interesting → investigate it.")
    print("If it is not interesting → move on.")

    print()
    print("=" * 68)


# ============================================================
# MODES
# ============================================================

def quick_mode(resources, history):
    category = choose_category(resources, history)

    resource = choose_resource(
        resources,
        category,
        history
    )

    mission = choose_mission(resource)

    add_history(
        history,
        resource,
        mission,
        "quick"
    )

    display_pick(
        resource,
        mission,
        "quick"
    )


def deep_mode(resources, history):
    category = choose_category(resources, history)

    resource = choose_resource(
        resources,
        category,
        history
    )

    mission = choose_mission(resource)

    display_pick(
        resource,
        mission,
        "deep"
    )

    print()
    print("DEEP INVESTIGATION CANVAS")
    print("-" * 68)
    print("Fill these in as far as you can. Blank is allowed.")
    print()

    investigation = {
        "signal": input("Signal identified        : ").strip(),
        "question": input("Question written        : ").strip(),
        "primary_source": input("Primary source found    : ").strip(),
        "triangulation": input("Triangulation performed : ").strip(),
        "hands_on": input("Hands-on investigation  : ").strip(),
        "understanding": input("Understanding            : ").strip(),
        "result": input("Result documented       : ").strip(),
        "artifact": input("Artifact created        : ").strip(),
    }

    history = add_history(
        history,
        resource,
        mission,
        "deep",
        investigation=investigation
    )

    print()
    print("DEEP MODE STATE SAVED")
    print("-" * 68)
    completed = sum(bool(value) for value in investigation.values())
    print(f"Completed fields : {completed}/{len(investigation)}")
    print("History contains the investigation state for continuation.")
    print()


def weekly_mode(resources, history):
    print()
    print("=" * 68)
    print("                    📅 WEEKLY RADAR")
    print("=" * 68)

    used_categories = set()
    weekly_entries = []

    all_categories = sorted({
        category
        for resource in resources
        for category in resource.get("categories", [])
    })

    if not all_categories:
        print("[!] No categories available.")
        return

    for i in range(5):
        available_categories = [
            category
            for category in all_categories
            if category not in used_categories
        ]

        if not available_categories:
            available_categories = all_categories

        category = random.choice(available_categories)
        used_categories.add(category)

        resource = choose_resource(
            resources,
            category,
            history
        )
        mission = choose_mission(resource)

        entry = {
            "day": i + 1,
            "category": category,
            "resource_id": resource.get("id"),
            "resource": resource.get("name"),
            "type": resource.get("type"),
            "regions": resource.get("regions", []),
            "mission": mission,
        }
        weekly_entries.append(entry)

        print()
        print(f"DAY {i + 1}")
        print("-" * 68)
        print(f"Category : {category}")
        print(f"Resource : {resource.get('name', '?')}")
        print(f"Type     : {resource.get('type', '?')}")
        print(f"Regions  : {', '.join(resource.get('regions', [])) or '-'}")
        print(f"Mission  : {mission}")

        history = add_history(
            history,
            resource,
            mission,
            "weekly"
        )

    week = datetime.now().date().isoformat()
    weekly_radar = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "mode": "weekly_summary",
        "record_type": "weekly_summary",
        "week": week,
        "interesting_signals": weekly_entries,
        "most_interesting": None,
        "why": None,
        "investigation_question": None,
        "sources": [entry["resource_id"] for entry in weekly_entries],
        "evidence": [],
        "hands_on": [],
        "result": None,
        "artifact": None,
        "publish": False,
    }

    history.append(weekly_radar)
    if len(history) > HISTORY_LIMIT:
        del history[:-HISTORY_LIMIT]
    save_history(history)

    print()
    print("WEEKLY INVESTIGATION CANVAS")
    print("-" * 68)
    print(f"Week                  : {week}")
    print("Most interesting      : [fill after the week]")
    print("Why                   : [fill after the week]")
    print("Investigation question: [fill after the week]")
    print(f"Sources               : {len(weekly_entries)} selected resources")
    print("Evidence              : [add evidence]")
    print("Hands-on              : [add investigation performed]")
    print("Result                : [fill after the week]")
    print("Artifact              : [fill after the week]")
    print("Publish               : false")
    print()
    print("=" * 68)

def list_mode(resources):
    print()
    print("=" * 68)
    print("                    📚 RESOURCE LIST")
    print("=" * 68)

    if not resources:
        print("[!] No resources available.")
        return

    for i, resource in enumerate(resources, 1):
        name = resource.get("name", "?")
        resource_type = resource.get("type", "?")
        tier = resource.get("tier", "?")

        categories = resource.get("categories", [])
        regions = resource.get("regions", [])

        print()
        print(f"[{i}] {name}")
        print(f"    Type       : {resource_type}")
        print(f"    Tier       : {tier}")
        print(
            f"    Categories : "
            f"{', '.join(categories) if categories else '-'}"
        )
        print(
            f"    Regions    : "
            f"{', '.join(regions) if regions else '-'}"
        )

        domain = resource.get("domain")
        path = resource.get("path", "")

        if domain:
            scheme = resource.get("scheme", "https")
            print(f"    Link       : {scheme}://{domain}{path}")
        else:
            print("    Link       : Search manually")

    print()
    print("=" * 68)
    print(f"Total resources: {len(resources)}")
    print("=" * 68)


def types_mode(resources):
    counts = {}

    for resource in resources:
        rtype = resource["type"]

        counts[rtype] = counts.get(
            rtype,
            0
        ) + 1

    print()
    print("=" * 68)
    print("                    RESOURCE TYPES")
    print("=" * 68)

    for rtype, count in sorted(
        counts.items(),
        key=lambda x: (-x[1], x[0])
    ):
        print(
            f"{rtype:<30} {count}"
        )

    print()
    print(f"Total resource types: {len(counts)}")
    print()


def history_mode(history):
    print()
    print("=" * 68)
    print("                    🕘 PICKER HISTORY")
    print("=" * 68)

    if not history:
        print("[!] No history yet.")
        return

    for i, item in enumerate(reversed(history), 1):
        timestamp = item.get("timestamp", "?")
        resource = item.get("resource", "?")
        resource_type = item.get("type", "?")
        tier = item.get("tier", "?")
        mission = item.get("mission", "?")
        mode = item.get("mode", "?")

        categories = item.get("categories", [])
        regions = item.get("regions", [])

        print()
        print(f"[{i}] {timestamp}")
        print(f"    Mode       : {mode}")
        print(f"    Resource   : {resource}")
        print(f"    Type       : {resource_type}")
        print(f"    Tier       : {tier}")
        print(
            f"    Categories : "
            f"{', '.join(categories) if categories else '-'}"
        )
        print(
            f"    Regions    : "
            f"{', '.join(regions) if regions else '-'}"
        )

        investigation = item.get("investigation")
        if investigation:
            completed = sum(bool(investigation.get(field)) for field in DEEP_INVESTIGATION_FIELDS)
            print(f"    Investigation: {completed}/{len(DEEP_INVESTIGATION_FIELDS)} fields completed")
            for field in CORE_LOOP_FIELDS:
                if field in investigation:
                    print(f"      {field:<16}: {investigation.get(field) or '-'}")
            if "result" in investigation and "result" not in CORE_LOOP_FIELDS:
                print(f"      {'result':<16}: {investigation.get('result') or '-'}")
            if "artifact" in investigation and "artifact" not in CORE_LOOP_FIELDS:
                print(f"      {'artifact':<16}: {investigation.get('artifact') or '-'}")
        print(f"    Mission    : {mission}")

    print()
    print("=" * 68)
    print(f"History entries: {len(history)}")
    print("=" * 68)


def stats_mode(resources, history):
    print()
    print("=" * 68)
    print("                    📊 PICKER STATS")
    print("=" * 68)

    print()
    print(f"Resources : {len(resources)}")
    print(f"History   : {len(history)}")

    # ------------------------------------------------------------
    # Resource statistics
    # ------------------------------------------------------------

    type_counts = {}
    category_counts = {}
    region_counts = {}
    tier_counts = {}

    for resource in resources:
        resource_type = resource.get("type")
        if resource_type:
            type_counts[resource_type] = (
                type_counts.get(resource_type, 0) + 1
            )

        tier = resource.get("tier")
        if tier:
            tier_counts[tier] = tier_counts.get(tier, 0) + 1

        for category in resource.get("categories", []):
            category_counts[category] = (
                category_counts.get(category, 0) + 1
            )

        for region in resource.get("regions", []):
            region_counts[region] = (
                region_counts.get(region, 0) + 1
            )

    # ------------------------------------------------------------
    # History statistics
    # ------------------------------------------------------------

    mode_counts = {}
    mission_counts = {}

    for item in history:
        mode = item.get("mode")
        if mode:
            mode_counts[mode] = mode_counts.get(mode, 0) + 1

        mission = item.get("mission")
        if mission:
            mission_counts[mission] = (
                mission_counts.get(mission, 0) + 1
            )

    # ------------------------------------------------------------
    # Display helper
    # ------------------------------------------------------------

    def print_counts(title, counts):
        print()
        print(title)
        print("-" * 68)

        if not counts:
            print("  -")
            return

        for key, count in sorted(
            counts.items(),
            key=lambda item: (-item[1], item[0])
        ):
            print(f"  {key:<35} {count}")

    # ------------------------------------------------------------
    # Display
    # ------------------------------------------------------------

    print_counts("RESOURCE TYPES", type_counts)
    print_counts("CATEGORIES", category_counts)
    print_counts("REGIONS", region_counts)
    print_counts("TIERS", tier_counts)

    print_counts("PICKER MODES", mode_counts)
    print_counts("MISSIONS", mission_counts)

    print()
    print("=" * 68)


# ============================================================
# SEARCH
# ============================================================

def search_mode(resources, query=None):
    print()
    print("=" * 68)
    print("                    🔎 RESOURCE SEARCH")
    print("=" * 68)

    if query is None:
        query = input("Search: ").strip()

    query = str(query).strip().lower()

    if not query:
        print("[!] Search query cannot be empty.")
        return

    results = []

    for resource in resources:
        name = str(resource.get("name", "")).lower()
        resource_type = str(resource.get("type", "")).lower()
        tier = str(resource.get("tier", "")).lower()

        categories = [
            str(category).lower()
            for category in resource.get("categories", [])
        ]

        regions = [
            str(region).lower()
            for region in resource.get("regions", [])
        ]

        searchable = " ".join([
            name,
            resource_type,
            tier,
            *categories,
            *regions,
        ])

        if query in searchable:
            results.append(resource)

    if not results:
        print()
        print("[!] No matching resources found.")
        return

    print()
    print(f"Found {len(results)} resource(s):")
    print("-" * 68)

    for i, resource in enumerate(results, 1):
        name = resource.get("name", "?")
        resource_type = resource.get("type", "?")
        tier = resource.get("tier", "?")

        categories = resource.get("categories", [])
        regions = resource.get("regions", [])

        print()
        print(f"[{i}] {name}")
        print(f"    Type       : {resource_type}")
        print(f"    Tier       : {tier}")
        print(
            f"    Categories : "
            f"{', '.join(categories) if categories else '-'}"
        )
        print(
            f"    Regions    : "
            f"{', '.join(regions) if regions else '-'}"
        )

        domain = resource.get("domain")
        path = resource.get("path", "")

        if domain:
            scheme = resource.get("scheme", "https")
            print(f"    Link       : {scheme}://{domain}{path}")
        else:
            print("    Link       : Search manually")

    print()
    print("=" * 68)

# ============================================================
# CATEGORY MODE
# ============================================================

def category_mode(resources, history, category):
    matches = [
        resource
        for resource in resources
        if category.lower() in [
            value.lower()
            for value in resource.get("categories", [])
        ]
    ]

    if not matches:
        print()
        print(f"[!] Category not found: {category}")
        print()
        print("Available categories:")

        categories = sorted({
            value
            for resource in resources
            for value in resource.get("categories", [])
        })

        for value in categories:
            print(f"  - {value}")

        print()
        return

    resource = choose_resource(
        matches,
        category,
        history
    )

    mission = choose_mission(resource)

    add_history(
        history,
        resource,
        mission,
        "category"
    )

    display_pick(
        resource,
        mission,
        f"category:{category}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description="Cybersecurity Radar Resource Picker"
    )

    parser.add_argument(
        "mode",
        nargs="?",
        default="quick",
        choices=[
            "quick",
            "deep",
            "weekly",
            "list",
            "types",
            "history",
            "stats",
            "search",
            "category"
        ]
    )

    parser.add_argument(
        "value",
        nargs="?"
    )

    args = parser.parse_args()

    resources = load_resources()
    history = load_history()

    if args.mode == "quick":

        quick_mode(
            resources,
            history
        )

    elif args.mode == "deep":

        deep_mode(
            resources,
            history
        )

    elif args.mode == "weekly":

        weekly_mode(
            resources,
            history
        )

    elif args.mode == "list":

        list_mode(
            resources
        )

    elif args.mode == "types":

        types_mode(
            resources
        )

    elif args.mode == "history":

        history_mode(
            history
        )

    elif args.mode == "stats":

        stats_mode(
            resources,
            history
        )

    elif args.mode == "search":

        if not args.value:

            print(
                "[!] Usage: "
                "python randomizer.py search <keyword>"
            )

            return

        search_mode(
            resources,
            args.value
        )

    elif args.mode == "category":

        if not args.value:

            print(
                "[!] Usage: "
                "python randomizer.py category <category>"
            )

            return

        category_mode(
            resources,
            history,
            args.value
        )


if __name__ == "__main__":
    main()