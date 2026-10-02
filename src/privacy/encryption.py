try:
    import tenseal as ts
    TENSEAL_AVAILABLE = True
except ImportError:
    TENSEAL_AVAILABLE = False
    ts = None

import numpy as np
import os

CONTEXT_PATH = "shared_context.tenseal"


def create_context():
    if not TENSEAL_AVAILABLE:
        raise RuntimeError("TenSEAL is not installed. Cannot create encryption context.")
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    context.global_scale = 2**40
    return context


def get_shared_context():
    """Loads the shared context from disk, or creates one if missing.
    In this simulation, client and server share one context to represent
    the key infrastructure a real deployment would manage separately."""
    if not TENSEAL_AVAILABLE:
        raise RuntimeError("TenSEAL is not installed. Cannot load or create encryption context.")
    if os.path.exists(CONTEXT_PATH):
        with open(CONTEXT_PATH, "rb") as f:
            return ts.context_from(f.read())
    context = create_context()
    with open(CONTEXT_PATH, "wb") as f:
        f.write(context.serialize(save_secret_key=True))
    return context


def encrypt_array(context, array):
    if not TENSEAL_AVAILABLE:
        raise RuntimeError("TenSEAL is not installed. Cannot encrypt array.")
    flat = array.flatten().tolist()
    return ts.ckks_vector(context, flat)


def decrypt_array(encrypted, original_shape):
    if not TENSEAL_AVAILABLE:
        raise RuntimeError("TenSEAL is not installed. Cannot decrypt array.")
    decrypted_flat = np.array(encrypted.decrypt())
    return decrypted_flat.reshape(original_shape)


def serialize_encrypted(enc_vector):
    if not TENSEAL_AVAILABLE:
        raise RuntimeError("TenSEAL is not installed. Cannot serialize encrypted vector.")
    return np.frombuffer(enc_vector.serialize(), dtype=np.uint8)


def deserialize_encrypted(context, byte_array):
    if not TENSEAL_AVAILABLE:
        raise RuntimeError("TenSEAL is not installed. Cannot deserialize encrypted vector.")
    return ts.ckks_vector_from(context, byte_array.tobytes())


def is_tenseal_available():
    return TENSEAL_AVAILABLE
