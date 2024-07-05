## URL Shablonlari va Dokumentatsiya

### Foydalanuvchilar

#### Foydalanuvchilar ro'yxati
- **URL:** `/api/v1/users/`
- **Metod:** `GET`, `POST`
- **Ruxsat etilgan foydalanuvchilar:** Superuser, Filial admini
- **Tavsif:** Barcha foydalanuvchilar ro'yxatini oling.

#### Foydalanuvchi Tafsilotlari
- **URL:** `/api/v1/users/<int:pk>/`
- **Metod:** `GET`, `PUT`, `DELETE`
- **Ruxsat etilgan foydalanuvchilar:** Superuser, Filial admini, Foydalanuvchi (o'zini)
- **Tavsif:** ID orqali aniq foydalanuvchini ko'rish, yangilash yoki o'chirish.

### Filiallar

#### Filiallar ro'yxati
- **URL:** `/api/v1/branches/`
- **Metod:** `GET`, `POST`
- **Ruxsat etilgan foydalanuvchilar:** Superuser, Filial admini
- **Tavsif:** Barcha filiallar ro'yxatini oling.

#### Filial Tafsilotlari
- **URL:** `/api/v1/branches/<int:pk>/`
- **Metod:** `GET`, `PUT`, `DELETE`
- **Ruxsat etilgan foydalanuvchilar:** Superuser, Filial admini
- **Tavsif:** ID orqali aniq filialni ko'rish, yangilash yoki o'chirish.

### Fanlar

#### Fanlar ro'yxati
- **URL:** `/api/v1/subjects/`
- **Metod:** `GET`, `POST`
- **Ruxsat etilgan foydalanuvchilar:** Superuser, Filial admini
- **Tavsif:** Barcha fanlar ro'yxatini oling.

#### Fan Tafsilotlari
- **URL:** `/api/v1/subjects/<int:pk>/`
- **Metod:** `GET`, `PUT`, `DELETE`
- **Ruxsat etilgan foydalanuvchilar:** Superuser, Filial admini
- **Tavsif:** ID orqali aniq fanlarni ko'rish, yangilash yoki o'chirish.

### Sinflar

#### Sinflar ro'yxati
- **URL:** `/api/v1/classes/`
- **Metod:** `GET`, `POST`
- **Ruxsat etilgan foydalanuvchilar:** Superuser, Filial admini
- **Tavsif:** Barcha sinflar ro'yxatini oling.

#### Sinf Tafsilotlari
- **URL:** `/api/v1/classes/<int:pk>/`
- **Metod:** `GET`, `PUT`, `DELETE`
- **Ruxsat etilgan foydalanuvchilar:** Superuser, Filial admini
- **Tavsif:** ID orqali aniq sinfni ko'rish, yangilash yoki o'chirish.

### Dars Jadvali

#### Dars jadvallari ro'yxati
- **URL:** `/api/v1/class-schedules/`
- **Metod:** `GET`, `POST`
- **Ruxsat etilgan foydalanuvchilar:** Superuser, Filial admini, O'qituvchi
- **Tavsif:** Barcha dars jadvallari ro'yxatini oling.

#### Dars jadvali Tafsilotlari
- **URL:** `/api/v1/class-schedules/<int:pk>/`
- **Metod:** `GET`, `PUT`, `DELETE`
- **Ruxsat etilgan foydalanuvchilar:** Superuser, Filial admini, O'qituvchi
- **Tavsif:** ID orqali aniq dars jadvalini ko'rish, yangilash yoki o'chirish.

### So'rovlar

#### So'rovlar ro'yxati
- **URL:** `/api/v1/requests/`
- **Metod:** `GET`, `POST`
- **Ruxsat etilgan foydalanuvchilar:** Superuser, Filial admini, O'qituvchi, Talaba
- **Tavsif:** Barcha so'rovlar ro'yxatini oling.

#### So'rov Tafsilotlari
- **URL:** `/api/v1/requests/<int:pk>/`
- **Metod:** `GET`, `PUT`, `DELETE`
- **Ruxsat etilgan foydalanuvchilar:** Superuser, Filial admini, O'qituvchi, Talaba (o'zini)
- **Tavsif:** ID orqali aniq so'rovni ko'rish, yangilash yoki o'chirish.

### Davomat olish
- **URL:** `/api/v1/class-schedule/<int:class_schedule_id>/attendance/take/`
- **Metod:** `GET`, `POST`
- **Ruxsat etilgan foydalanuvchilar:** Superuser, Filial admini, O'qituvchi
- **Tavsif:** Aniq dars jadvali uchun davomat ma'lumotlarini Pastdagi najmunadan foydalanib yuboring.

#### Namuna So'rov Body:
```json
{
    "attendance": [
        {
            "student": 4,
            "class_schedule": 456,
            "attended": false,
            "date": "2024-07-05"
        },
        {
            "student": 7,
            "class_schedule": 456,
            "attended": false,
            "date": "2024-07-05"
        }
    ]
}
