from __future__ import annotations

CORE_CAPABILITIES = {
    'repository': ['repo_init','repo_clone','repo_inventory','repo_export','repo_diff'],
    'workspace': ['file_create','file_read','file_update','file_delete','file_copy','file_move','zip_import','zip_integrate'],
    'engineering': ['requirements_graph','capability_graph','architecture_plan','implementation_plan','evidence_pack'],
    'intelligence': ['browser_frontier_cowork','openai_compatible_model','mock_model'],
    'quality': ['deterministic_validation','frontier_benchmark','security_gate','portability_test','repair_loop'],
    'cyber_physical': ['digital_thread','world_model','safety_supervisor','edge_control_boundary'],
}

PROVIDER_ADAPTER_EXAMPLES = {
    'git_hosting': ['github','gitlab','forgejo','generic_git'],
    'model_access': ['frontier_browser','openai_compatible','local_openai_compatible'],
    'compute': ['generic_linux','docker','kubernetes','serverless'],
    'data': ['sql','document','object_storage'],
    'events': ['queue','event_stream','event_log'],
}

def registry():
    return {'version':'0.1.0','core_capabilities':CORE_CAPABILITIES,'provider_adapter_examples':PROVIDER_ADAPTER_EXAMPLES}
