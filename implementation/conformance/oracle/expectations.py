from __future__ import annotations

from typing import Dict, Any, Optional

"""
This module provides a set of high-level expectation functions to be used
when building the `expected_trace` for a test case.

These functions act as a Domain Specific Language (DSL) for writing tests,
making them more readable and less prone to errors. Each function is a simple
factory that returns a dictionary matching the event structure the TraceOracle expects.
"""

# --- Workflow Lifecycle Expectations ---

def expect_workflow_start(workflow_code: Optional[str] = None) -> Dict[str, Any]:
    """
    Generates an expectation for the 'workflow_start' event.
    
    Args:
        workflow_code: If provided, asserts the 'workflow_code' field matches.
    """
    event = {"event": "workflow_start"}
    if workflow_code:
        event["workflow_code"] = workflow_code
    return event

def expect_workflow_complete(
    workflow_code: Optional[str] = None,
    result_status: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates an expectation for the 'workflow_complete' event.
    
    Args:
        workflow_code: If provided, asserts the 'workflow_code' field matches.
        result_status: If provided, asserts the 'result_status' field matches.
    """
    event = {"event": "workflow_complete"}
    if workflow_code:
        event["workflow_code"] = workflow_code
    if result_status:
        event["result_status"] = result_status
    return event


# --- Node Execution Expectations ---

def expect_node_start(node_code: str) -> Dict[str, Any]:
    """

    Generates an expectation for a 'node_start' event.
    
    Args:
        node_code: The expected code of the node being entered.
    """
    return {"event": "node_start", "node_code": node_code}


def expect_node_end(node_code: str, result_status: str) -> Dict[str, Any]:
    """
    Generates an expectation for a 'node_end' event.
    
    Args:
        node_code: The expected code of the node finishing.
        result_status: The expected result status of the node.
    """
    return {
        "event": "node_end",
        "node_code": node_code,
        "result_status": result_status,
    }


# --- Capability-related Expectations ---

def expect_capability_start(capability_code: str) -> Dict[str, Any]:
    """
    Generates an expectation for a 'capability_start' event.
    
    Args:
        capability_code: The expected code of the capability being invoked.
    """
    return {"event": "capability_start", "capability_code": capability_code}


def expect_capability_end(
    capability_code: str,
    result_status: str
) -> Dict[str, Any]:
    """
    Generates an expectation for a 'capability_end' event.
    
    Args:
        capability_code: The expected code of the capability finishing.
        result_status: The expected result status of the capability.
    """
    return {
        "event": "capability_end",
        "capability_code": capability_code,
        "result_status": result_status,
    }
