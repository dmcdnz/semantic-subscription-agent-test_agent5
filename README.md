# {agent_name}

{description}

## Configuration

This agent is configured in `config.yaml`. Key settings include:

- Interest threshold: {threshold}
- Classifier enabled: {classifier_enabled}
- Polling interval: {polling_interval} seconds

## Usage

To test this agent individually:

```bash
# Test the agent directly
python agents/{package_name}/agent.py

# Test using the framework
python test_framework.py agent {package_name}
```

## Customization

Edit `agent.py` to implement your domain-specific processing logic in the `process_message` method.

If needed, you can customize the interest model by modifying `interest_model.py`.

## Example Integration

```python
from semsubscription.core import MessageBus
from semsubscription.core import AgentManager

# The agent will be automatically discovered and registered
AgentManager.discover_agents()

# Process a message that might interest this agent
message_id = MessageBus.add_message("Your message here")
responses = MessageBus.get_responses(message_id)
print(responses)
```
