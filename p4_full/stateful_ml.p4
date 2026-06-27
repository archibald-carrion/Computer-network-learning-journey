
#include <core.p4>
#include <v1model.p4>

/* =========================
   CONSTANTS
========================= */

const bit<32> REG_SIZE = 1024;

/* =========================
   REGISTERS
========================= */

register<bit<32>>(REG_SIZE) pkt_count;
register<bit<32>>(REG_SIZE) total_bytes;
register<bit<48>>(REG_SIZE) first_seen;

/* =========================
   HEADERS / METADATA
========================= */

struct headers { }

struct metadata_t {
    bit<1> is_high;
};

/* =========================
   PARSER
========================= */

parser MyParser(packet_in packet,
                out headers hdr,
                inout metadata_t meta,
                inout standard_metadata_t standard_metadata) {
    state start {
        transition accept;
    }
}

/* =========================
   VERIFY CHECKSUM
========================= */

control MyVerifyChecksum(inout headers hdr,
                         inout metadata_t meta) {
    apply { }
}

/* =========================
   INGRESS
========================= */

control MyIngress(inout headers hdr,
                  inout metadata_t meta,
                  inout standard_metadata_t standard_metadata) {

    apply {

        /* -------- FLOW INDEX -------- */
        bit<32> index;

        hash(index, HashAlgorithm.crc32, (bit<32>)0,
             { standard_metadata.ingress_port },
             REG_SIZE);

        /* -------- STATE -------- */
        bit<32> count;
        bit<32> bytes;
        bit<48> first;
        bit<48> now;

        now = standard_metadata.ingress_global_timestamp;

        pkt_count.read(count, index);
        count = count + 1;
        pkt_count.write(index, count);

        total_bytes.read(bytes, index);
        bytes = bytes + standard_metadata.packet_length;
        total_bytes.write(index, bytes);

        first_seen.read(first, index);

        if (first == 0) {
            first_seen.write(index, now);
            first = now;
        }

        /* -------- FEATURES (NO DIVISION) -------- */

        bit<48> duration;
        duration = now - first;

        bit<1> high_rate;
        bit<1> large_avg;

        /* Rate: count/duration > 700 pkt/s  --> count * 1_000_000 > 700 * duration */
        if (((bit<64>)count * 1000000) > (700 * (bit<64>)duration)) {
            high_rate = 1;
        } else {
            high_rate = 0;
        }

        /* Avg: bytes > (1000 * count) */
        if (bytes > (1000 * count)) {
            large_avg = 1;
        } else {
            large_avg = 0;
        }

        /* -------- DECISION TREE -------- */

        if (high_rate == 1) {
            if (large_avg == 1) {
                meta.is_high = 1;
            } else {
                meta.is_high = 0;
            }
        } else {
            if (duration < 1000) {
                meta.is_high = 1;
            } else {
                meta.is_high = 0;
            }
        }

        /* -------- FORWARDING -------- */

        if (meta.is_high == 0) {
            if (standard_metadata.ingress_port == 1) {
                standard_metadata.egress_spec = 2;
            } else if (standard_metadata.ingress_port == 2) {
                standard_metadata.egress_spec = 1;
            }
        } else {
            mark_to_drop(standard_metadata);
        }
    }
}

/* =========================
   EGRESS
========================= */

control MyEgress(inout headers hdr,
                 inout metadata_t meta,
                 inout standard_metadata_t standard_metadata) {
    apply { }
}

/* =========================
   COMPUTE CHECKSUM
========================= */

control MyComputeChecksum(inout headers hdr,
                          inout metadata_t meta) {
    apply { }
}

/* =========================
   DEPARSER
========================= */

control MyDeparser(packet_out packet,
                   in headers hdr) {
    apply { }
}

/* =========================
   SWITCH
========================= */

V1Switch(
    MyParser(),
    MyVerifyChecksum(),
    MyIngress(),
    MyEgress(),
    MyComputeChecksum(),
    MyDeparser()
) main;
