class TestConfig:
    server_host:str = "http://127.0.0.1"
    server_port:int = 8000
    server_prefix:str = "/api/v1/"
    server_full_path:str = f"{server_host}:{server_port}{server_prefix}"