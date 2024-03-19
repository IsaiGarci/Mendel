def CalculteIfDifferenceIsTip(Total, ImporteFacturado):
    Total = float(Total.replace("$", "").replace(",", ""))
    ImporteFacturado = float(ImporteFacturado.replace("$", "").replace(",", ""))

    Difference = Total - ImporteFacturado
    
    if ImporteFacturado > 0:
        DifferencePercentage = (Difference / ImporteFacturado) * 100
    else:
        DifferencePercentage = 0
    
    
    if 1 <= DifferencePercentage <= 15:
        Tip = Difference
        Excess = 0
    elif DifferencePercentage > 15:
        Tip = ImporteFacturado * 0.15
        Excess = Difference - Tip
    else:
        Tip = 0
        Excess = Difference
    
    return Tip, Excess