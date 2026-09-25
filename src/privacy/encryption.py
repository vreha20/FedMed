import tenseal as ts
import numpy as np

def create_context():
    """Creates a TenSEAL CKKS context for homomorphic encryption."""
    context = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60]
    )
    context.generate_galois_keys()
    context.global_scale = 2**40
    return context


def encrypt_array(context, array):
    """Encrypts a numpy array (flattened) using CKKS."""
    flat = array.flatten().tolist()
    encrypted = ts.ckks_vector(context, flat)
    return encrypted


def decrypt_array(encrypted, original_shape):
    """Decrypts back to a numpy array with the original shape."""
    decrypted_flat = np.array(encrypted.decrypt())
    return decrypted_flat.reshape(original_shape)
