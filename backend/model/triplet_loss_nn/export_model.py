import tensorflow as tf
import os

from backend.server.model import SiameseNetworkModel

model = SiameseNetworkModel('backend/model/train_hard_mining/cp.ckpt').embedding_model

MODEL_DIR = 'backend/model/exported_model'
version = 1
export_path = os.path.join(MODEL_DIR, str(version))
print('export_path = {}\n'.format(export_path))

tf.keras.models.save_model(
    model,
    export_path,
    overwrite=True,
    include_optimizer=True,
    save_format=None,
    signatures=None,
    options=None
)

print('\nSaved model:')

