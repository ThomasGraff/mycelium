from typing import Optional
from os import getenv
from supabase import Client, create_client

class SupabaseManager:
    """
    Manages Supabase client configuration and connection.
    """
    _instance: Optional['SupabaseManager'] = None
    _client: Optional[Client] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.supabase_url = getenv('SUPABASE_URL')
            self.supabase_key = getenv('SUPABASE_KEY')
            self.initialized = True

    def initialize_client(self) -> None:
        """
        Initializes the Supabase client if not already initialized.
        """
        if not self._client and self.supabase_url and self.supabase_key:
            self._client = create_client(self.supabase_url, self.supabase_key)

    @property
    def client(self) -> Client:
        """
        Returns the Supabase client instance.
        
        :return: Supabase client
        :raises ValueError: If Supabase is not properly configured
        """
        if not self._client:
            if not (self.supabase_url and self.supabase_key):
                raise ValueError("Supabase configuration is missing. Please set SUPABASE_URL and SUPABASE_KEY environment variables.")
            self.initialize_client()
        return self._client

supabase_manager = SupabaseManager() 