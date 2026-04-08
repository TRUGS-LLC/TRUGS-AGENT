

# --- Edge Cases & Common Mistakes ---

def test_empty_nodes_list():
    """Empty nodes list should fail validation."""
    t = _make(nodes=[], edges=[])
    r = validate(t)
    assert not r.valid


def test_orphan_edge_no_from_node():
    """Edge references non-existent from_id."""
    t = _make(
        nodes=[{"id": "a", "type": "DATA", "properties": {}, "parent_id": None, "contains": [], "metric_level": "BASE_DATA", "dimension": "a"}],
        edges=[{"from_id": "nonexistent", "to_id": "a", "relation": "READ"}],
    )
    r = validate(t)
    assert not r.valid
    assert "ORPHAN_EDGE" in _errors(r)


def test_orphan_edge_no_to_node():
    """Edge references non-existent to_id."""
    t = _make(
        nodes=[{"id": "a", "type": "DATA", "properties": {}, "parent_id": None, "contains": [], "metric_level": "BASE_DATA", "dimension": "a"}],
        edges=[{"from_id": "a", "to_id": "nonexistent", "relation": "READ"}],
    )
    r = validate(t)
    assert not r.valid
    assert "ORPHAN_EDGE" in _errors(r)


def test_duplicate_ids_same_node_list():
    """Duplicate IDs in nodes list."""
    t = _make(
        nodes=[
            {"id": "dup", "type": "DATA", "properties": {}, "parent_id": None, "contains": [], "metric_level": "BASE_DATA", "dimension": "d1"},
            {"id": "dup", "type": "DATA", "properties": {}, "parent_id": None, "contains": [], "metric_level": "BASE_DATA", "dimension": "d2"},
        ]
    )
    r = validate(t)
    assert not r.valid
    assert "DUPLICATE_ID" in _errors(r)


def test_missing_id_field():
    """Node missing id field."""
    t = _make(nodes=[{"type": "DATA", "properties": {}, "parent_id": None, "contains": [], "metric_level": "BASE_DATA", "dimension": "d"}])
    r = validate(t)
    assert not r.valid


def test_missing_type_field():
    """Node missing type field."""
    t = _make(nodes=[{"id": "a", "properties": {}, "parent_id": None, "contains": [], "metric_level": "BASE_DATA", "dimension": "a"}])
    r = validate(t)
    assert not r.valid


def test_circular_containment_self_reference():
    """Node contains itself."""
    t = _make(
        nodes=[{"id": "a", "type": "PIPELINE", "properties": {}, "parent_id": None, "contains": ["a"], "metric_level": "BASE_PIPELINE"}]
    )
    r = validate(t)
    assert not r.valid
    assert "CIRCULAR_CONTAINMENT" in _errors(r)


def test_circular_containment_two_nodes():
    """Two nodes contain each other."""
    t = _make(
        nodes=[
            {"id": "a", "type": "PIPELINE", "properties": {}, "parent_id": None, "contains": ["b"], "metric_level": "BASE_PIPELINE"},
            {"id": "b", "type": "PIPELINE", "properties": {}, "parent_id": None, "contains": ["a"], "metric_level": "BASE_PIPELINE"},
        ]
    )
    r = validate(t)
    assert not r.valid
    assert "CIRCULAR_CONTAINMENT" in _errors(r)


def test_invalid_parent_id_reference():
    """Node parent_id references non-existent node."""
    t = _make(
        nodes=[{"id": "a", "type": "DATA", "properties": {}, "parent_id": "nonexistent", "contains": [], "metric_level": "BASE_DATA", "dimension": "a"}]
    )
    r = validate(t)
    assert not r.valid


def test_invalid_contains_reference():
    """Node contains references non-existent node."""
    t = _make(
        nodes=[{"id": "a", "type": "PIPELINE", "properties": {}, "parent_id": None, "contains": ["nonexistent"], "metric_level": "BASE_PIPELINE"}]
    )
    r = validate(t)
    assert not r.valid


def test_null_id():
    """Node has null id."""
    t = _make(nodes=[{"id": None, "type": "DATA", "properties": {}, "parent_id": None, "contains": [], "metric_level": "BASE_DATA", "dimension": "d"}])
    r = validate(t)
    assert not r.valid


def test_empty_string_id():
    """Node has empty string id."""
    t = _make(nodes=[{"id": "", "type": "DATA", "properties": {}, "parent_id": None, "contains": [], "metric_level": "BASE_DATA", "dimension": "d"}])
    r = validate(t)
    assert not r.valid


def test_deeply_nested_containment():
    """Test deeply nested parent-child relationships."""
    nodes = [
        {"id": "root", "type": "PIPELINE", "properties": {}, "parent_id": None, "contains": ["level1"], "metric_level": "BASE_PIPELINE"},
        {"id": "level1", "type": "STAGE", "properties": {}, "parent_id": "root", "contains": ["level2"], "metric_level": "BASE_PIPELINE"},
        {"id": "level2", "type": "MODULE", "properties": {}, "parent_id": "level1", "contains": ["level3"], "metric_level": "BASE_PIPELINE"},
        {"id": "level3", "type": "NAMESPACE", "properties": {}, "parent_id": "level2", "contains": [], "metric_level": "BASE_PIPELINE"},
    ]
    t = _make(nodes=nodes)
    r = validate(t)
    assert r.valid


def test_edges_only_no_containment():
    """Graph with edges but no parent-child relationships."""
    t = _make(
        nodes=[
            {"id": "a", "type": "TRANSFORM", "properties": {}, "parent_id": None, "contains": [], "metric_level": "BASE_ACTOR"},
            {"id": "b", "type": "DATA", "properties": {}, "parent_id": None, "contains": [], "metric_level": "BASE_DATA", "dimension": "b"},
        ],
        edges=[{"from_id": "a", "to_id": "b", "relation": "READ"}],
    )
    r = validate(t)
    assert r.valid
