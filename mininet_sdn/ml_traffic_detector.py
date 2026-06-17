from pox.core import core
import pox.openflow.libopenflow_01 as of

import os
import pickle
import numpy as np

log = core.getLogger()


class MLTrafficDetector(object):

    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)

        # Load model from same directory as this script
        model_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "traffic_model.pkl"
        )

        log.info("Loading model from %s", model_path)

        log.info("Before pickle.load()")

        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

        log.info("After pickle.load()")

        self._request_stats()

    def _request_stats(self):
        log.info("Requesting flow stats")

        self.connection.send(
            of.ofp_stats_request(
                body=of.ofp_flow_stats_request()
            )
        )

        core.callDelayed(5, self._request_stats)

    def _handle_FlowStatsReceived(self, event):

        try:

            log.info(
                "Received FlowStats reply containing %d flows",
                len(event.stats)
            )

            for stat in event.stats:

                duration = stat.duration_sec + (
                    stat.duration_nsec / 1e9
                )

                if duration <= 0:
                    continue

                packet_count = stat.packet_count
                byte_count = stat.byte_count

                byte_rate = byte_count / duration
                packet_rate = packet_count / duration

                avg_pkt_size = (
                    byte_count / packet_count
                    if packet_count > 0 else 0
                )

                features = np.array([
                    [
                        packet_count,
                        byte_count,
                        stat.duration_sec,
                        stat.duration_nsec,
                        byte_rate,
                        packet_rate,
                        avg_pkt_size
                    ]
                ])


                log.info(
                    "Features: pkt=%d bytes=%d duration=%.2f pkt_rate=%.2f byte_rate=%.2f avg=%0.2f",
                    packet_count,
                    byte_count,
                    duration,
                    packet_rate,
                    byte_rate,
                    avg_pkt_size
                )

                prediction = self.model.predict(features)[0]

                log.info("Prediction = %d", prediction)

                if prediction == 1:
                    log.warning("HIGH TRAFFIC detected: %s", stat.match)

                    # Install DROP rule
                    msg = of.ofp_flow_mod()
                    msg.match = stat.match

                    msg.priority = 100
                    msg.idle_timeout = 30
                    msg.hard_timeout = 60

                    # No actions = DROP
                    msg.actions = []

                    self.connection.send(msg)

                    log.warning(
                        "Installed DROP rule for suspicious flow: %s",
                        stat.match
                    )

                else:
                    log.info("Normal traffic: %s", stat.match)

        except Exception:
            import traceback
            log.error(traceback.format_exc())


def launch():

    def start_switch(event):
        log.info("Switch connected: %s", event.connection)
        MLTrafficDetector(event.connection)

    core.openflow.addListenerByName(
        "ConnectionUp",
        start_switch
    )