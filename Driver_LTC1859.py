import spidev
import RPi.GPIO as IO
import time

class LTC1859:
    def __init__(self, bus=0, device=0, max_speed_hz=1000000, mode=0b00,convst=16):
        """
        Initialisation du bus SPI et des paramètres de l'ADC LTC1859
        params:
        :param bus: Numéro du bus SPI
        :param device: Numéro du périphérique SPI
        :param max_speed_hz: Vitesse maximale du bus SPI en Hz
        :param mode: Mode SPI (0b00 à 0b11)
        """
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)
        self.spi.max_speed_hz = max_speed_hz
        self.spi.mode = mode
        self.convst=convst
        IO.setmode(IO.BOARD)
        IO.setwarnings(False)
        IO.setup(self.convst,IO.OUT,initial=IO.LOW)

    def read_channel(self, channel):
        """
        Lit les données d'un canal spécifié du LTC1859
        :param channel: Numéro du canal (0 à 7)
        :return: Valeur numérique lue depuis le canal ADC
        """
        if not (0 <= channel <= 7):
            raise valueError("Channel must be between 0 and 7.")
        command= 0x8000 | (channel << 11)
        IO.output(self.convst,IO.HIGH)
        time.sleep(0.001)
        IO.output(self.convst,IO.LOW)
        # Envoyer la commande de lecture SPI et recevoir la réponse

        self.spi.xfer2([(command >> 8) & 0xFF,command & 0xFF])
        time.sleep(0.001)
        adc = self.spi.xfer2([0x00,0x00])
        print(f"réponse brute : {adc}")

        # Convertir les deux derniers octets en une valeur numérique
        data = ((adc[0] & 0xFF) << 8) | (adc[1] & 0xFF)
        return data

    def close(self):
        # Fermer la connexion SPI
        self.spi.close()
        IO.cleanup(self.convst)

# Exemple d'utilisation de la classe LTC1859
if __name__ == "__main__":
    adc = LTC1859()
    try:
        channel = 0  # Spécifiez le canal que vous voulez lire
        data = adc.read_channel(channel)
        print(f"Données lues depuis le canal SPI {channel}: {data}")
    finally:
        adc.close()
