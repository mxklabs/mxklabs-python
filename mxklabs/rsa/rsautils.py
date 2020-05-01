import asn1tools
import base64 
import os
import struct

class RsaUtils:

  # Get the ASN.1 schema filename.
  _asn1_filename = os.path.join(os.path.dirname(__file__), 'rfc3447.asn')
  # Create an ASN.1 parser and decode the binary_data.
  _asn1_parser = asn1tools.compile_files(_asn1_filename)

  @staticmethod
  def _getChunk(binary_data):
    """ Convenience function for extracting a field. """

    # Get the first four bytes to see how big the field is.
    chunk_len = struct.unpack('>I', binary_data[:4])[0]
    # Get the field data and return the field data and remaining bytes.
    chunk = binary_data[4:4+chunk_len]
    remaining_binary_data = binary_data[4+chunk_len:]
    return chunk, remaining_binary_data

  @staticmethod
  def publicKeyFromFile(filename):
    """ Extract public key file contents as a dictionary. """

    # Read file and extract base64.
    file_as_str = open(filename, 'r').read()
    file_parts = file_as_str.split(' ')
    binary_data = base64.b64decode(file_parts[1])

    # Discard the key type.
    _, binary_data = RsaUtils._getChunk(binary_data)
    # Get the public exponent.
    public_exponent_as_bytes, binary_data = RsaUtils._getChunk(binary_data)
    public_exponent = int.from_bytes(public_exponent_as_bytes, byteorder='big')
    # Get the modulus.
    modulus_as_bytes, binary_data = RsaUtils._getChunk(binary_data)
    modulus = int.from_bytes(modulus_as_bytes, byteorder='big')

    return { 'publicExponent': public_exponent, 'modulus' : modulus }

  @staticmethod
  def privateKeyFromFile(filename):
    """ Extract private key file contents as a dictionary. """

    # Read the file.
    file_as_str = open(filename, 'r').read()
    # Tokenise the file on spaces.
    lines = file_as_str.split('\n')
    binary_data = base64.b64decode("".join(lines[1:-2]))

    # Decode the ASN.1.
    return RsaUtils._asn1_parser.decode('RSAPrivateKey', binary_data)