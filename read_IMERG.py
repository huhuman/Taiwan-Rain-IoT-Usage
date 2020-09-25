from netCDF4 import Dataset
import os


def readIMERGdata(dataset_root):
    files = os.listdir(dataset_root)
    paths = [os.path.join(dataset_root, filename)
             for filename in files if filename.endswith('.nc4')]
    latest_file = max(paths, key=os.path.getctime)
    print(latest_file)
    dataset = Dataset(latest_file, 'r')
    print(dataset.variables['precipitationCal'][0].shape)
    dataset.close()


def main():
    root_IMERG = './IMERG/2020-09-15/'
    readIMERGdata(root_IMERG)


if __name__ == "__main__":
    main()
