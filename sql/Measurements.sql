Select g.yarnTestHeight, yarnTestWidth, gc.measurements
FROM Garment AS g
JOIN garmentconstruction AS gc ON g.id = gc.GarmentID
