mport spidev

class LTC1859:
    def __init__(self, bus=0, device=0, max_speed_hz=1000000, mode=0b00):
        """
        Initialisation du bus SPI et des paramètres de l'ADC LTC1859
        :param bus: Numéro du bus SPI
        :param device: Numéro du périphérique SPI
        :param max_speed_hz: Vitesse maximale du bus SPI en Hz
        :param mode: Mode SPI (0b00 à 0b11)
        """
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = max_speed_hz
        self.spi.mode = mode

    def read_channel(self, channel):
        """
        Lit les données d'un canal spécifié du LTC1859
        :param channel: Numéro du canal (0 à 7)
        :return: Valeur numérique lue depuis le canal ADC
        """
        if not (0 <= channel <= 7):
            raise ValueError("Channel must be between 0 and 7.")
        # Envoyer la commande de lecture SPI et recevoir la réponse
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
        # Convertir les deux derniers octets en une valeur numérique
        data = ((adc[1] & 3) << 8) + adc[2]
        return data

    def close(self):
        # Fermer la connexion SPI
        self.spi.close()

# Exemple d'utilisation de la classe LTC1859
if __name__ == "__main__":
    adc = LTC1859()
    try:
        channel = 0  # Spécifiez le canal que vous voulez lire
        data = adc.read_channel(channel)
        print(f"Données lues depuis le canal SPI {channel}: {data}")
    finally:
        adc.close()