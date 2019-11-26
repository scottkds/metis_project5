from keras.models import Model

# note we exclude the final dense layers and add one back below, we would retrain it ourselves
base_model = VGG16(weights='imagenet', include_top=False, input_shape=(3,224,224))

# Freeze convolutional layers
for layer in base_model.layers:
    layer.trainable = False

x = base_model.output
x = Flatten()(x) # flatten from convolution tensor output
predictions = Dense(2, activation='softmax')(x) # should match # of classes predicted

# this is the model we will train
model = Model(inputs=base_model.input, outputs=predictions)
