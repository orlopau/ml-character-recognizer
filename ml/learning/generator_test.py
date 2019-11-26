import image_retriever
import matplotlib.pyplot as plt

generators = image_retriever.retrieve_images('../imgs/')
trainer = generators['train']

p = trainer.next()

print(p)

plt.imshow(p[0][0][:, :, 0], cmap='gray')
plt.show()
