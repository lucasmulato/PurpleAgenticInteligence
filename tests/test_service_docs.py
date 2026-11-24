"""Fase 3: consistência mínima do pacote de serviço (documentação)."""
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
SERVICE = ROOT / "service"

EXPECTED = [
    "AUDITORIA.md",
    "templates/relatorio.md",
    "templates/politica.example.yaml",
    "checklist-inventario.md",
    "vertical-financeiro.md",
    "one-pager.pt.md",
    "one-pager.en.md",
    "parceria-whitelabel.md",
    "lgpd-checklist.md",
]


def test_all_service_files_exist():
    for rel in EXPECTED:
        assert (SERVICE / rel).exists(), rel


def test_checklist_has_at_most_15_questions():
    text = (SERVICE / "checklist-inventario.md").read_text(encoding="utf-8")
    questions = re.findall(r"^\d+\. ", text, flags=re.MULTILINE)
    assert 1 <= len(questions) <= 15


def test_no_compliance_guarantee_phrase():
    for rel in EXPECTED:
        text = (SERVICE / rel).read_text(encoding="utf-8")
        affirmative = text.replace("não garante", "").replace("Não garante", "")
        assert not re.search(r"garante conformidade", affirmative, re.I), rel
        assert "formally verified" not in text.lower(), rel


def test_no_prices_in_service_docs():
    for rel in EXPECTED:
        text = (SERVICE / rel).read_text(encoding="utf-8")
        assert "R$" not in text, rel


def test_one_pagers_have_required_sections():
    pt = (SERVICE / "one-pager.pt.md").read_text(encoding="utf-8")
    en = (SERVICE / "one-pager.en.md").read_text(encoding="utf-8")
    assert "Problema" in pt and "Contato" in pt
    assert "Problem" in en and "Contact" in en


def test_example_policy_is_valid_for_safe_ai():
    parsed = yaml.safe_load(
        (SERVICE / "templates" / "politica.example.yaml").read_text(encoding="utf-8")
    )
    assert set(parsed) == {"permit", "ask_human", "reject"}
    assert "curl" in parsed["reject"]
