SELECT g.id, g.name, gt.name
FROM garment AS g
JOIN garmenttype AS gt ON gt.id = g.garmenttypeid