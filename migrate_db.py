import pymysql

def migrate():
    try:
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            db='smartelectro',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            # Check Order table
            try:
                cursor.execute("ALTER TABLE `order` ADD COLUMN payment_method VARCHAR(50) DEFAULT 'Cash On Delivery'")
                print("Added payment_method to order table")
            except Exception as e:
                print(f"order table adjustment: {e}")
            
            # Check User table for OTP columns
            try:
                cursor.execute("ALTER TABLE `user` ADD COLUMN reset_otp VARCHAR(10)")
                cursor.execute("ALTER TABLE `user` ADD COLUMN otp_expiry DATETIME")
                print("Added OTP columns to user table")
            except Exception as e:
                print(f"user table adjustment: {e}")
                
            # Check PrivacySetting table
            try:
                cursor.execute("ALTER TABLE privacy_setting ADD COLUMN data_sharing BOOLEAN DEFAULT 1")
                cursor.execute("ALTER TABLE privacy_setting ADD COLUMN profile_visibility VARCHAR(50) DEFAULT 'Public'")
                print("Added privacy columns")
            except Exception as e:
                print(f"privacy table adjustment: {e}")

            conn.commit()
        conn.close()
        print("Migration finished!")
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
