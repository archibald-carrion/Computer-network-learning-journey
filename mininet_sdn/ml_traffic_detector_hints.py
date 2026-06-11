from pox.core import core
import pox.openflow.libopenflow_01 as of

import pickle
import numpy as np

log = core.getLogger()

class MLTrafficDetector(object):

    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)

        with open("traffic_model.pkl", "rb") as f:
            self.model = pickle.load(f)

        self._request_stats()

    def _request_stats(self):
        self.connection.send(of.ofp_stats_request(
            body=of.ofp_flow_stats_request()
        ))
        core.callDelayed(5, self._request_stats)

    def _handle_FlowStatsReceived(self, event):
        for stat in event.stats:

            duration = stat.duration_sec + stat.duration_nsec / 1e9
            if duration == 0:
                continue

            packet_count = stat.packet_count
            byte_count = stat.byte_count

            byte_rate = byte_count / duration
            packet_rate = packet_count / duration

            avg_pkt_size = byte_count / packet_count if packet_count > 0 else 0

            features = np.array([[packet_count, byte_count, stat.duration_sec,
                                  stat.duration_nsec, byte_rate,
                                  packet_rate, avg_pkt_size]])

            prediction = self.model.predict(features)[0]

            if prediction == 1:
                log.warning(f"HIGH TRAFFIC detected: {stat.match}")

                # === STUDENT TASK ===
                # 1. Create flow_mod
                # 2. Match stat.match
                # 3. Set priority + timeouts
                # 4. Leave actions empty (DROP)
                # 5. Send rule

            else:
                log.info(f"Normal traffic: {stat.match}")


def launch():
    def start_switch(event):
        MLTrafficDetector(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
