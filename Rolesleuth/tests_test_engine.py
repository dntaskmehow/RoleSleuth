import unittest
from rolesleuth.config import AuditConfig, Role, TargetRequest
from rolesleuth.engine import AuditEngine

class TestAuditEngine(unittest.TestCase):
    def test_engine_initialization(self):
        config = AuditConfig(
            target_base_url="https://example.com",
            roles=[
                Role(name="Admin", cookies={"session": "admin123"}),
                Role(name="User", cookies={"session": "user123"})
            ]
        )
        reqs = [TargetRequest(method="GET", url="https://example.com/api/profile")]
        engine = AuditEngine(config, reqs)
        self.assertEqual(len(engine.requests_list), 1)

if __name__ == "__main__":
    unittest.main()