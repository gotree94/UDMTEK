"""
UDMTEK Backend API Routes
"""

from . import plc_parser
from . import udml_translator
from . import ai_analysis
from . import dashboard

__all__ = ['plc_parser', 'udml_translator', 'ai_analysis', 'dashboard']
