import unittest
from unittest.mock import Mock, patch

import server


class IncidentHubMCPTests(unittest.TestCase):
    @patch("server._request")
    def test_list_incidents_filters_service_and_status(self, request):
        request.return_value = [
            {"id": "INC-1", "service": "checkout", "status": "open"},
            {"id": "INC-2", "service": "billing", "status": "open"},
            {"id": "INC-3", "service": "checkout", "status": "resolved"},
        ]

        result = server.list_incidents(service="checkout", status="open")

        self.assertEqual([item["id"] for item in result], ["INC-1"])
        request.assert_called_once_with("GET", "/api/incidents")

    @patch("server._request")
    def test_get_incident_returns_matching_record(self, request):
        request.return_value = [{"id": "INC-42", "title": "Checkout latency"}]

        self.assertEqual(server.get_incident("INC-42")["title"], "Checkout latency")

    @patch("server._request")
    def test_get_incident_rejects_unknown_id(self, request):
        request.return_value = []

        with self.assertRaisesRegex(ValueError, "Incident not found"):
            server.get_incident("missing")

    @patch("server._request")
    def test_checkout_summary_is_read_only_get(self, request):
        request.return_value = {"service": "checkout", "open_incidents": 1}

        self.assertEqual(server.get_checkout_summary()["open_incidents"], 1)
        request.assert_called_once_with("GET", "/api/checkout/summary")

    @patch("server._request")
    def test_acknowledge_incident_is_post(self, request):
        request.return_value = {"id": "INC-42", "status": "acknowledged"}

        result = server.acknowledge_incident("INC-42")

        self.assertEqual(result["status"], "acknowledged")
        request.assert_called_once_with("POST", "/api/incidents/INC-42/ack")

    def test_rejects_empty_incident_id(self):
        with self.assertRaises(ValueError):
            server.get_incident("")


if __name__ == "__main__":
    unittest.main()
