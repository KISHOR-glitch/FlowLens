from langchain.tools import tool

from processminer.sql_tools.bottleneck import bottleneck_analysis
from processminer.sql_tools.kpi import kpi_dashboard
from processminer.sql_tools.process_discovery import process_discovery
from processminer.sql_tools.resources import resource_analysis
from processminer.sql_tools.sla import sla_detection
from processminer.sql_tools.variants import variant_analysis


@tool
def bottleneck_tool():
    """Finds bottlenecks in the business process."""
    return str(bottleneck_analysis())


@tool
def kpi_tool():
    """Retrieves the KPI dashboard."""
    return str(kpi_dashboard())


@tool
def process_discovery_tool():
    """Discovers the process flow from the event log."""
    return str(process_discovery())


@tool
def resource_tool():
    """Analyzes resource workload and processing times."""
    return str(resource_analysis())


@tool
def sla_tool():
    """Detects SLA violations in the business process."""
    return str(sla_detection())


@tool
def variant_tool():
    """Analyzes process variants for all orders."""
    return str(variant_analysis())