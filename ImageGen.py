from PIL import Image
import os

class ImageGen:
    def __init__(self, image = None):
        self.path = './ham_eaten_jellybear/assets/images/post/'
        if image:
            self.name = image.split('.')[0]
            self.format = image.split('.')[-1]
            self.image = Image.open('./ham_eaten_jellybear/assets/images/post/'+image)
        else:
            self.image = None

    def toWebp(self):
        self.image.save(self.path + self.name + '.webp', 'webp')
        os.remove(self.path + self.name + '.' + self.format)

    def toWebpAll(self):
        for i in os.listdir(self.path):
            if i.split('.')[-1] != 'webp':
                print(i)
                im = Image.open(f'{self.path}/{i}')
                im.save(f'{self.path}/{i.split(".")[0]}.webp', 'webp')

                os.remove(f'{self.path}/{i}')

                os.system(f'find ./ham_eaten_jellybear/_posts -type f -name "*.md" -exec sed -i \'s/{i}/{i.split(".")[0]}.webp/g\' "{{}}" \;')
        
if __name__ == "__main__":
    imageGen = ImageGen()
    imageGen.toWebpAll()