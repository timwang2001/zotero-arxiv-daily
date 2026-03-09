from types import SimpleNamespace

from zotero_arxiv_daily.retriever.arxiv_retriever import (
    filter_papers_by_rules,
    paper_matches_rules,
)


def test_paper_matches_rules_include_only():
    paper = SimpleNamespace(title="A diffusion model", summary="for image generation")
    assert paper_matches_rules(paper, ["diffusion"], None)
    assert not paper_matches_rules(paper, ["transformer"], None)


def test_paper_matches_rules_exclude_only():
    paper = SimpleNamespace(title="A survey of models", summary="for image generation")
    assert not paper_matches_rules(paper, None, ["survey"])
    assert paper_matches_rules(paper, None, ["benchmark"])


def test_paper_matches_rules_include_and_exclude():
    paper = SimpleNamespace(title="Multimodal benchmark", summary="with diffusion")
    assert not paper_matches_rules(paper, ["diffusion"], ["benchmark"])
    assert paper_matches_rules(paper, ["multimodal"], ["survey"])


def test_filter_papers_by_rules_fallback_to_unfiltered_when_empty():
    papers = [
        SimpleNamespace(title="Paper A", summary="about optimization"),
        SimpleNamespace(title="Paper B", summary="about retrieval"),
    ]

    filtered = filter_papers_by_rules(papers, ["diffusion"], None)

    assert filtered == papers


def test_filter_papers_by_rules_keep_filtered_when_not_empty():
    papers = [
        SimpleNamespace(title="Diffusion Paper", summary="about generation"),
        SimpleNamespace(title="Retriever", summary="about search"),
    ]

    filtered = filter_papers_by_rules(papers, ["diffusion"], None)

    assert len(filtered) == 1
    assert filtered[0].title == "Diffusion Paper"
