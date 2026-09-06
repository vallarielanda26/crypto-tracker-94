class CryptoTrackerError(Exception):
    """Base exception for the crypto-tracker-94 ecosystem."""
    pass

class NetworkGlitch(CryptoTrackerError):
    """Raised when the blockchain whispers nonsense."""
    pass

class WalletDrain(CryptoTrackerError):
    """Raised when funds vanish into the void."""
    pass

class ProtocolMismatch(CryptoTrackerError):
    """Raised when the handshake fails hard."""
    pass

def handle_crypto_chaos(error: Exception) -> dict:
    """Translates existential dread into structured chaos responses."""
    mapping = {
        NetworkGlitch: "retrying_connection_sequence",
        WalletDrain: "initiating_emergency_shutdown_protocol",
        ProtocolMismatch: "recalculating_node_compatibility"
    }
    action = mapping.get(type(error), "panic_and_log_stacktrace")
    
    return {
        "status": "unstable",
        "reaction": action,
        "error_type": error.__class__.__name__,
        "suggestion": "check_nodes_for_sunspots"
    }

if __name__ == "__main__":
    try:
        raise NetworkGlitch("The network is having a bad day.")
    except CryptoTrackerError as e:
        print(handle_crypto_chaos(e))