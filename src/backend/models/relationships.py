from sqlalchemy import Table, Integer, ForeignKey, Column

from config.database import Base

agent_tool_association = Table(
    'agent_tool_association',
    Base.metadata,
    Column('agent_id', Integer, ForeignKey('agents.id')),
    Column('tool_id', Integer, ForeignKey('tools.id'))
)

tool_llm_association = Table(
    'tool_llm_association',
    Base.metadata,
    Column('tool_id', Integer, ForeignKey('tools.id')),
    Column('llm_id', Integer, ForeignKey('llms.id'))
)
