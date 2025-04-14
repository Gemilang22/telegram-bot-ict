@dp.message(F.photo)
async def get_photo_file_id(message: types.Message):
    # Ambil foto dengan resolusi tertinggi
    photo = message.photo[-1]
    
    # Kirim file ID ke pengguna
    await message.reply(f"File ID gambar QRIS kamu: `{photo.file_id}`", parse_mode="Markdown")
