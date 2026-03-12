# config.py
# This file is a placeholder for configuration management.
# In a real application, you would likely use a more robust
# configuration management system (e.g., a configuration file,
# environment variables, or a dedicated configuration library).
# This example demonstrates the basic concept of loading
# configuration values from a dictionary.
import os

config = {
    'database_url': 'sqlite:///tasks.db',
    'debug': True,
    'api_key': os.environ.get('API_KEY', 'default_api_key')
}

# Example usage:
# print(config['database_url'])
# print(config['api_key'])