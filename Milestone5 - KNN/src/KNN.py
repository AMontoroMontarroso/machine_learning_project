import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn import neighbors

def training():
	n_train = 150
	validation_error= [0] * 151
	trainingG= []
	testG = []
	latlon1 = []
	latlon2 = []
	zone1 = []
	zone2 = []
	with open('out/zones_random_60.csv','r') as training_group:
		with open('out/zones_random_40.csv','r') as test_group:
			for aux_train in training_group:
				chain1 = aux_train.split(";")
				trainingG = [chain1[0],chain1[1],chain1[2]]
				data_latlon1=[chain1[0],chain1[1]]
				data_zone1=[chain1[2].replace("\n", "")]
				latlon1.append(data_latlon1)
				zone1.append(data_zone1)
			for aux_test in test_group:
				chain2 = aux_test.split(";")
				testG = [chain2[0],chain2[1],chain2[2]]
				data_latlon2 = [chain2[0],chain2[1]]
				data_zone2=[chain2[2].replace("\n", "")]
				latlon2.append(data_latlon2)
				zone2.append(data_zone2)

	for n_neighbors in range(1,151):
		clf = neighbors.KNeighborsClassifier(n_neighbors, weights='distance')
		clf.fit(latlon1, zone1)
		Z = clf.predict(latlon2)
		aux = 0
		for i in range(len(zone2)):
			if(zone2[i] != Z[i]):
				aux += 1

		error = aux/ len(zone2)

		validation_error[n_neighbors] += error
		temp = list(map(lambda x : x / n_train, validation_error))
		validation_error=temp


	plt.title('Selection of best K (distance)')
	plt.ylabel('Error')
	plt.xlabel('K')
	plt.xlim(1, 200)
	plt.ylim(-0.002,0.002)
	plt.plot(validation_error)
	plt.show()

	K = len(validation_error) - list(reversed(validation_error)).index(min(validation_error[1:])) - 1
	print ('Best K is: %d' % K)

	latitude = []
	longitude = []
	latitude_longitude = []
	zone = []

	with open('out/zones.csv', 'r') as latlonzon:

		for aux in latlonzon:
			cad = aux.split(";")
			latitudeAux = [cad[0]]
			longitudeAux = [cad[1]]
			latitude_longitudeAux = [cad[0],cad[1]]
			zoneAux = [cad[2].replace("\n", "")]
			latitude.append(latitudeAux)
			longitude.append(longitudeAux)
			latitude_longitude.append(latitude_longitudeAux)
			zone.append(zoneAux)

	cmap = ListedColormap(plt.cm.Paired(np.linspace(0, 1, len(np.unique(Z)))))


	clf = neighbors.KNeighborsClassifier(K, weights='distance')
	clf.fit(latitude_longitude,zone)

	latitude_min = float(min(min(latitude))) - 0.01
	latitude_max = float(max(max(latitude))) + 0.01

	longitude_min = float(min(min(longitude))) - 0.01
	longitude_max = float(max(max(longitude))) + 0.01

	h = 1  # step size in the mesh

	np_arrange_lat = np.arange(latitude_min, latitude_max, h)
	np_arrange_lon = np.arange(longitude_max, longitude_min, h)

	latCoor, lonCoor = np.meshgrid(np_arrange_lat, np_arrange_lon)

	Z = clf.predict(np.c_[latCoor.ravel(),lonCoor.ravel()])
	Z = Z.reshape(latCoor.shape)


	plt.figure()
	plt.pcolormesh(latCoor, lonCoor, Z, cmap = cmap)
	plt.scatter(latitude, longitude, c = zone, cmap = cmap)
	plt.xlim(latitude_min, latitude_max)
	plt.ylim(longitude_min, longitude_max)
	plt.title("Classification zone where k = %d, weights = 'distance'" %(K))
	plt.show()


	latitudes = list()
	longitudes = list()
	for line in open('out/works_normalised.csv').readlines():
		line_split = line.split(";")
		latitudes.append(line_split[0])
		longitudes.append(line_split[1])


	clf_works = neighbors.KNeighborsClassifier(K, weights='distance')
	clf_works.fit(latitude_longitude, zone)
	Z = clf_works.predict(np.c_[latitudes, longitudes])

	Z_vector = [x for x in Z]

	with open('out/works_normalised.csv', 'r') as works_in:
		with open('out/works_zones.csv','w') as works_out:

			counter = 0
			works_out.write("Latitude;Longitude;Zone\n")
			for line in works_in:
				line_out = line[:-1] + ';' + Z_vector[counter] + "\n"
				works_out.write(line_out)
				counter += 1

training()
