from threading import Thread
import time
import random
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusDeviceContext, ModbusServerContext

SLAVE_ID = 0

STORE_CO = 1
CO_CHARGER = 0

STORE_DI = 2
DI_HIGH_TENSION = 0
DI_LOW_TENSION = 1

STORE_IR = 4
IR_TEMPERATURE = 0

# -------- Simulation de la température --------
def temperature_simulation(context, slave_id=SLAVE_ID):
    tension = 36
    charger_on = False
    while True:
        # Lire l'état du chauffage
        charger_on = bool(context[slave_id].getValues(STORE_CO, CO_CHARGER, count=1)[0])  # Coil 0

        # Faire varier la tension
        if heating_on:
            tension += random.uniform(0.4, 0.9)
        else:
            tension -= random.uniform(0.3, 0.7)

        # bornes
        if tension < 30:
            tension = 30
        if tension > 42:
            tension = 42

        # Écrire dans registre (Input Register 0, valeur entière)
        context[slave_id].setValues(STORE_IR, IR_TEMPERATURE, [int(tension)]) 

        # Capteurs discrets
        high_tension = 1 if temperature > 42 else 0
        low_tension = 1 if temperature < 30 else 0

        context[slave_id].setValues(STORE_DI, DI_HIGH_TENSION, [high_tension)  # DI0
        context[slave_id].setValues(STORE_DI, DI_LOW_TENSION, [low_tension])   # DI1

        # Affichage console
        print(f"T = {temperature:.1f} °C | Chargeur={'ON' if charger_on else 'OFF'} | >42={high_tension} | <30={low_tension}")

        time.sleep(1)



if __name__ == "__main__":
    # -------- Configuration initiale --------
    # Coil 0 = bouton chauffage (ON/OFF)
    # Discrete Inputs:
    #   DI 0 = capteur > 42V
    #   DI 1 = capteur < 30V
    # Input Register 0 = température courante (°C * 10 pour garder 1 décimale si besoin)

    store = ModbusDeviceContext(
        di=ModbusSequentialDataBlock(SLAVE_ID, [0] * 10),
        co=ModbusSequentialDataBlock(SLAVE_ID, [0] * 10),
        hr=ModbusSequentialDataBlock(SLAVE_ID, [0] * 10),
        ir=ModbusSequentialDataBlock(SLAVE_ID, [0] * 10)
    )

    context = ModbusServerContext(devices=store, single=True)

    # Lancement du thread de simulation de température
    sim_thread = Thread(target=temperature_simulation, args=(context,))
    sim_thread.daemon = True
    sim_thread.start()

    # Démarrage du serveur Modbus TCP sur le port 502
    print("Serveur Modbus TCP démarré sur le port 502...")
    StartTcpServer(context, address=("0.0.0.0", 502))
