#GCS-01,02をSerailポートから制御するコードのテスト
#GCS-01,02とPCは送受信とハードウェアフロー制御が必要で，ストレートケーブルで接続すること
#今どき，CTS-RTSのハードウェアフロー制御を行っていることが注意
#PySerialのテストで，間違ってもテストコード名をSerial.pyにしてはいけない
#2025/01/04　野間

import serial
import time

def main():
    # シリアルポートの設定
    comport_xy = "COM3"  # 使用するシリアルポートを指定（例: COM3、/dev/ttyUSB0など）
    comport_z = "COM4"
    rate = 9600
    timeout = 1  # タイムアウト設定（秒）

    try:
        # シリアルポートを開く
        ser_xy = serial.Serial(
            port=comport_xy,
            baudrate=rate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            xonxoff=False,  # ソフトウェアフロー制御無効
            rtscts=True,  # ハードウェアフロー制御有効
            timeout=timeout
        )

        ser_z = serial.Serial(
            port=comport_z,
            baudrate=rate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            xonxoff=False,  # ソフトウェアフロー制御無効
            rtscts=True,  # ハードウェアフロー制御有効
            timeout=timeout
        )
        
        if ser_xy.is_open:
            print(f"シリアルポート {comport_xy} が開きました。")
    
    
        if ser_z.is_open:
            print(f"シリアルポート {comport_z} が開きました。")

        # 確認コマンドを送信
        confirmation_command_cal = "H:W+-\r\n"  # キャリブレーション
        confirmation_command_speed = "D:2S1000F20000R100S1000F20000R100\r\n"  # 速度設定
        confirmation_command_1 = "M:1-P80000\r\n"  # コマンドのフォーマットに応じて修正
        confirmation_command_2 = "G:\r\n"  # 駆動開始
        #print(f"コマンド送信: {confirmation_command_cal.strip()}")
        #ser_xy.write(confirmation_command_cal.encode('utf-8'))
        print(f"コマンド送s信: {confirmation_command_1.strip()}")
        ser_xy.write(confirmation_command_1.encode('utf-8'))
        print(f"コマンド送信: {confirmation_command_2.strip()}")
        ser_xy.write(confirmation_command_2.encode('utf-8'))

        #confirmation_command_Q = "Q:\r\n"  #状態確認
        #ser_xy.write(confirmation_command_Q.encode('utf-8'))
        #print(f"コマンド送信: {confirmation_command_Q.strip()}")

        time.sleep(2)

        confirmation_command_stop = "L:W\r\n"  #減速停止
        #ser_xy.write(confirmation_command_stop.encode('utf-8'))
        print(f"コマンド送信: {confirmation_command_stop.strip()}")

        #confirmation_command_Q = "Q:\r\n"  #ｚ軸の　状態確認
        #ser_xy.write(confirmation_command_Q.encode('utf-8'))
        #print(f"コマンド送信: {confirmation_command_Q.strip()}")
        #time.sleep(0.1)
        #response = ser_xy.read_all().decode('utf-8')
        #print(f"応答: {response.strip()}")
        #time.sleep(0)
        #response = ser_xy.read_all().decode('utf-8')
        #print(f"応答: {response.strip()}")
        confirmation_command_Q = "Q:\r\n"  #ｚ軸の　状態確認
        ser_xy.write(confirmation_command_Q.encode('utf-8'))
        print(f"コマンド送信: {confirmation_command_Q.strip()}")
        time.sleep(0.1)
        response = ser_xy.read_all().decode('utf-8')
        print(f"応答: {response.strip()}")

      

        # 確認コマンドを送信
        #confirmation_command = "H:1\r\n"  # コマンドのフォーマットに応じて修正
        #print(f"コマンド送信: {confirmation_command.strip()}")
        #ser.write(confirmation_command.encode('utf-8'))
        

        confirmation_command_zm = "M:1+P30000\r\n"  #z軸の移動量
        ser_xy.write(confirmation_command_zm.encode('utf-8'))
        print(f"コマンド送信: {confirmation_command_zm.strip()}")

        #confirmation_command_Q = "Q:\r\n"  #ｚ軸の　状態確認
        #ser_xy.write(confirmation_command_Q.encode('utf-8'))
        #print(f"コマンド送信: {confirmation_command_Q.strip()}")
        
        #response = ser_xy.read_all().decode('utf-8')
        #print(f"応答: {response.strip()}")

        confirmation_command_g = "G:\r\n"  #z軸駆動
        ser_xy.write(confirmation_command_g.encode('utf-8'))
        print(f"コマンド送信: {confirmation_command_g.strip()}")

        #confirmation_command_r = "R:1\r\n"  #z軸の原点指定
        #ser_z.write(confirmation_command_r.encode('utf-8'))
        #print(f"コマンド送信: {confirmation_command_r.strip()}")

        

        # 応答を受信
        #time.sleep(0.5)  # 少し待機して応答を待つ
        #response = ser_z.read_all().decode('utf-8')
        #print(f"応答: {response.strip()}")

    except serial.SerialException as e:
        print(f"シリアル通信エラー: {e}")

    finally:
        # シリアルポートを閉じる
        if 'ser' in locals() and ser.is_open:
            ser_xy.close()
            print(f"シリアルポート {comport_xy} を閉じました。")

if __name__ == "__main__":
    main()