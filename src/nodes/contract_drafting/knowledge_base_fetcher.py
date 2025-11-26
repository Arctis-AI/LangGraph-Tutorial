"""Knowledge base fetcher node for retrieving historical contracts and clauses."""

import os
from typing import Dict, Any
from src.models.contract_drafting_state import ContractDraftingState


def knowledge_base_fetcher_node(state: ContractDraftingState) -> Dict[str, Any]:
    """
    Fetch relevant contracts, clauses, and structures from Supabase.
    Store everything in state.

    If fetch fails, returns empty data and continues workflow without error.

    Args:
        state: Current workflow state

    Returns:
        Updates to state with retrieved knowledge base data
    """
    print("🔍 Fetching knowledge base data...")

    updates = {
        "current_step": "knowledge_base_fetcher",
        "messages": [],
        # Set defaults in case of failure
        "retrieved_contracts": [],
        "retrieved_clauses": [],
        "contract_structures": []
    }

    try:
        # Check if Supabase credentials are available
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")

        if not supabase_url or not supabase_key:
            print("⚠️ Supabase credentials not configured")
            updates["messages"].append({
                "role": "system",
                "content": "⚠️ Knowledge base not configured - proceeding without historical examples"
            })
            return updates

        # Import here to avoid errors if supabase package not installed
        from supabase import create_client, Client

        # Initialize Supabase client
        supabase: Client = create_client(supabase_url, supabase_key)

        contract_type_code = state.get("contract_type_code")
        project_description = state.get("project_description", "")

        # 1. Fetch similar contracts by type
        try:
            contracts_response = supabase.table("contracts") \
                .select("*") \
                .eq("contract_type_code", contract_type_code) \
                .limit(5) \
                .execute()

            updates["retrieved_contracts"] = contracts_response.data or []
        except Exception as e:
            print(f"⚠️ Could not fetch contracts: {e}")
            updates["retrieved_contracts"] = []

        # 2. Fetch example clauses for this contract type
        try:
            clauses_response = supabase.table("clauses") \
                .select("*") \
                .eq("contract_type_code", contract_type_code) \
                .limit(20) \
                .execute()

            updates["retrieved_clauses"] = clauses_response.data or []
        except Exception as e:
            print(f"⚠️ Could not fetch clauses: {e}")
            updates["retrieved_clauses"] = []

        # 3. Fetch contract structures
        try:
            structures_response = supabase.table("contract_structures") \
                .select("*") \
                .eq("contract_type_code", contract_type_code) \
                .execute()

            updates["contract_structures"] = structures_response.data or []
        except Exception as e:
            print(f"⚠️ Could not fetch structures: {e}")
            updates["contract_structures"] = []

        # 4. Optional: Semantic search by project description
        # If you have embeddings set up in the future
        if project_description and False:  # Disabled for now
            try:
                # embedding = get_embedding(project_description)
                # semantic_results = supabase.rpc("match_contracts", {
                #     "query_embedding": embedding,
                #     "match_threshold": 0.7,
                #     "match_count": 5
                # }).execute()
                # Merge with retrieved_contracts
                pass
            except Exception as e:
                print(f"⚠️ Semantic search failed: {e}")

        updates["messages"].append({
            "role": "system",
            "content": f"✓ Retrieved {len(updates['retrieved_contracts'])} contracts, "
                      f"{len(updates['retrieved_clauses'])} clauses, "
                      f"{len(updates['contract_structures'])} structures"
        })

    except ImportError:
        # Supabase package not installed
        print("⚠️ Supabase package not installed")
        updates["messages"].append({
            "role": "system",
            "content": "⚠️ Knowledge base library not available - proceeding without historical examples"
        })

    except Exception as e:
        # Log the error but don't fail the workflow
        print(f"⚠️ Knowledge base fetch failed: {str(e)}")
        updates["messages"].append({
            "role": "system",
            "content": f"⚠️ Knowledge base unavailable - proceeding without historical examples"
        })
        # Empty defaults already set above

    return updates
