#!/usr/bin/env python

"""
Test_agent5 Agent Implementation

test agent for semantic subscription
"""

import json
import logging
import os
import re
from typing import Dict, Any, Optional

# For containerized agents, use the local base agent
# This avoids dependencies on the semsubscription module
try:
    # First try to import from semsubscription if available (for local development)
    from semsubscription.agents.EnhancedAgent import EnhancedAgent as BaseAgent
except ImportError:
    try:
        # Fall back to local agent_base for containerized environments using relative import
        from .agent_base import BaseAgent
    except ImportError:
        # Last resort for Docker environment with current directory
        import sys
        import os
        # Add the current directory to the path to find agent_base.py
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from agent_base import BaseAgent

logger = logging.getLogger(__name__)

class Test_agent5Agent(BaseAgent):
    """
    Agent that test agent for semantic subscription
    """
    
    def __init__(self, agent_id=None, name=None, description=None, similarity_threshold=0.7, **kwargs):
        """
        Initialize the agent with its parameters and setup the classifier
        
        Args:
            agent_id: Optional unique identifier for the agent
            name: Optional name for the agent (defaults to class name)
            description: Optional description of the agent
            similarity_threshold: Threshold for similarity-based interest determination
        """
        # Set default name if not provided
        name = name or "Test_agent5 Agent"
        description = description or "test agent for semantic subscription"
        
        # Call parent constructor
        super().__init__(
            agent_id=agent_id,
            name=name,
            description=description,
            similarity_threshold=similarity_threshold,
            # Enable classifier by default for more accurate message routing
            use_classifier=True,  
            **kwargs
        )
        
        logger.info(f"{name} agent initialized")
    
    def setup_interest_model(self):
        """
        Set up the agent's interest model, which determines what messages it processes
        This is called automatically during initialization
        """
        # Call the parent method to set up the basic interest model
        super().setup_interest_model()
        
        # Here you can add specialized keyword matching or other domain-specific
        # interest determination logic
        
        # For example, to add keywords that should always be of interest:
        # self.interest_model.keywords.extend([
        #     "specific_keyword",
        #     "another_keyword"
        # ])
    
    def process_message(self, message) -> Optional[Dict[str, Any]]:
        """
        Process domain-specific queries
        
        Args:
            message: The message to process (dict in containerized version)
            
        Returns:
            Response data
        """
        try:
            # Handle both Message objects and dictionary messages (for container compatibility)
            if hasattr(message, 'content'):
                content = message.content
                message_id = getattr(message, 'id', 'unknown')
            else:
                content = message.get('content', '')
                message_id = message.get('id', 'unknown')
                
            query = content.lower()
            
            # Log the message being processed
            logger.info(f"Processing message {message_id} with content: '{content[:50]}...'")
            
            # Domain for {domain}
            # Add your domain-specific processing logic here
            
            # Example pattern matching for various domain queries
            if 'help' in query or 'hello' in query:
                return {
                    "agent": self.name,
                    "response": f"Hello! I'm {self.name}, an agent that {self.description.lower()}. How can I help you?"
                }
            elif '{domain}' in query:
                return {
                    "agent": self.name,
                    "response": f"I detected a {domain} related query: {content}"
                }
            #
            # Example:
            # if "weather" in query and ("forecast" in query or "today" in query):
            #     return {
            #         "agent": self.name,
            #         "query_type": "weather_forecast",
            #         "forecast": "Sunny with a high of 72Â°F"
            #     }}
            
            # Default response if no pattern matches
            return {
                "agent": self.name,
                "query_type": "general_response",
                "response": f"I received your query in the {domain} domain. This is a placeholder response."
            }
            
        except Exception as e:
            logger.error(f"Error in Test_agent5 Agent processing: {e}")
            return {
                "agent": self.name,
                "error": str(e),
                "query": content if 'content' in locals() else "unknown query"
            }


# For standalone testing
if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create the agent
    agent = Test_agent5Agent()
    print(f"Agent created: {agent.name}")
    
    # Test classifier setup
    print("\nClassifier Status:")
    if hasattr(agent, 'classifier_model') and hasattr(agent, 'classification_head'):
        print(f"  Classifier Model: Loaded successfully")
        print(f"  Classification Head: Loaded successfully")
        print(f"  Use Classifier: {agent.use_classifier}")
        print(f"  Classifier Threshold: {agent.classifier_threshold}")
    else:
        print("  Warning: Classifier not fully loaded!")
        if not hasattr(agent, 'classifier_model'):
            print("  - Missing classifier_model")
        if not hasattr(agent, 'classification_head'):
            print("  - Missing classification_head")
    
    # Test with sample messages
    test_messages = [
        "Your test query specific to this agent's domain",
        "A query that should probably not be handled by this agent",
        "Another domain-specific query to test routing"
    ]
    
    for i, test_message in enumerate(test_messages):
        print(f"\nTest {i+1}: '{test_message}'")
        
        # Test interest calculation
        from semsubscription.vector_db.database import Message
        message = Message(content=test_message)
        interest_score = agent.calculate_interest(message)
        
        print(f"Interest Score: {interest_score:.4f} (Threshold: {agent.similarity_threshold} for similarity, {agent.classifier_threshold} for classifier)")
        print(f"Agent would {'process' if interest_score >= max(agent.similarity_threshold, agent.classifier_threshold) else 'ignore'} this message")
        
        # If interested, test processing
        if interest_score >= max(agent.similarity_threshold, agent.classifier_threshold):
            result = agent.process_message(message)
            print("Processing Result:")
            print(json.dumps(result, indent=2))
            
    print("\nAgent testing complete.")

