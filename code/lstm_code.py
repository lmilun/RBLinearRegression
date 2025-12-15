import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout, Masking, Bidirectional, BatchNormalization, Layer
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score
import tensorflow.keras.backend as K
import matplotlib.pyplot as plt

# === Load data ===
X = np.load('data/X_LSTM.npy', allow_pickle=True)
y = np.load('data/y_LSTM.npy', allow_pickle=True)
player_ids = np.load('data/window_ids.npy', allow_pickle=True)

print(f"X shape: {X.shape}, y shape: {y.shape}")
num_features = X.shape[2]

# === Scale features individually ===
X_scaled = np.zeros_like(X, dtype='float32')
for i in range(num_features):
    feature = X[..., i]
    valid = feature != 0.0
    if np.any(valid):
        scaled_vals = (feature[valid] - feature[valid].mean()) / feature[valid].std()
        X_scaled[..., i][valid] = scaled_vals

# === Scale target ===
y = y.reshape(-1,1)
y_scaler = StandardScaler()
y_scaled = y_scaler.fit_transform(y).flatten()

# === Train/validation split by player ===
unique_players = np.unique(player_ids)
np.random.shuffle(unique_players)
split_p = int(0.8 * len(unique_players))
train_players = set(unique_players[:split_p])
train_mask = np.isin(player_ids, list(train_players))

X_train, X_val = X_scaled[train_mask], X_scaled[~train_mask]
y_train, y_val = y_scaled[train_mask], y_scaled[~train_mask]

print(f"Train size: {X_train.shape}, Val size: {X_val.shape}")

# === Attention layer ===
class Attention(Layer):
    def __init__(self, **kwargs):
        super(Attention, self).__init__(**kwargs)
    def build(self, input_shape):
        self.W = self.add_weight(name='att_weight', shape=(input_shape[-1],1),
                                 initializer='random_normal', trainable=True)
        self.b = self.add_weight(name='att_bias', shape=(input_shape[1],1),
                                 initializer='zeros', trainable=True)
        super(Attention, self).build(input_shape)
    def call(self, x):
        e = K.tanh(K.dot(x,self.W) + self.b)
        e = K.squeeze(e,-1)
        alpha = K.softmax(e)
        alpha = K.expand_dims(alpha,-1)
        context = x * alpha
        context = K.sum(context, axis=1)
        return context

# === Build over-parameterized model to risk overfitting ===
input_seq = Input(shape=(X.shape[1], X.shape[2]))
masked = Masking(mask_value=0.0)(input_seq)

lstm_out = Bidirectional(LSTM(256, return_sequences=True, dropout=0.4, recurrent_dropout=0.3))(masked)
lstm_out = BatchNormalization()(lstm_out)
lstm_out = Bidirectional(LSTM(128, return_sequences=True, dropout=0.4, recurrent_dropout=0.3))(lstm_out)
lstm_out = BatchNormalization()(lstm_out)

attn_out = Attention()(lstm_out)
dense = Dense(128, activation='relu')(attn_out)
dense = Dropout(0.4)(dense)
dense = Dense(64, activation='relu')(dense)
output = Dense(1)(dense)

model = Model(inputs=input_seq, outputs=output)
model.compile(optimizer='adam', loss='mse', metrics=['mae'])
model.summary()

# === Train ===
early_stop = EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True)
history = model.fit(X_train, y_train, validation_data=(X_val, y_val),
                    epochs=200, batch_size=16, callbacks=[early_stop], verbose=1)

# === Evaluate ===
y_pred_scaled = model.predict(X_val)
y_pred = y_scaler.inverse_transform(y_pred_scaled)
y_true = y_scaler.inverse_transform(y_val.reshape(-1,1))

r2 = r2_score(y_true, y_pred)
val_loss, val_mae = model.evaluate(X_val, y_val, verbose=0)
rmse = np.sqrt(val_loss) * y_scaler.scale_[0]
mae_unscaled = val_mae * y_scaler.scale_[0]

print(f"\nValidation RMSE: {rmse:.3f}")
print(f"Validation MAE:  {mae_unscaled:.3f}")
print(f"Validation R²:   {r2:.3f}")

# === Save model ===
model.save('data/lstm_model_attention_overfit.keras')

# === Plot training vs validation loss to show overfitting ===
plt.plot(history.history['loss'], label='Train MSE')
plt.plot(history.history['val_loss'], label='Val MSE')
plt.title('Training vs Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('MSE')
plt.legend()
plt.show()
