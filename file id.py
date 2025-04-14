import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

@dp.message(F.photo)
async def get_photo_file_id(message: types.Message):
    # Ambil foto dengan resolusi tertinggi
    photo = message.photo[-1]
    
    # Log file ID
    logging.info(f"File ID: {photo.file_id}")

    # Kirim file ID ke pengguna
    await message.reply(f"File ID gambar QRIS kamu: `{photo.file_id}`", parse_mode="Markdown")
