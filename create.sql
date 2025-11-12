CREATE TABLE Customer (
    ID SERIAL PRIMARY KEY,
    FirstName VARCHAR(50) NOT NULL,
    LastName VARCHAR(50) NOT NULL,
    Phone VARCHAR(15) NOT NULL,
    Email VARCHAR(100) NOT NULL UNIQUE,
    Address VARCHAR(255) NOT NULL
);

CREATE TABLE ClimateControl (
    ClimateControlled BOOLEAN PRIMARY KEY,
    MonthlyRate DECIMAL(10, 2) NOT NULL, 
    
    CONSTRAINT CheckClimateControlMonthlyRateValue CHECK (MonthlyRate >= 0)
);

CREATE TABLE StorageUnit (
    ID SERIAL PRIMARY KEY,
    Floor INTEGER NOT NULL 
    ClimateControlled BOOLEAN NOT NULL,
    
    CONSTRAINT CheckStorageUnitFloorValue CHECK (Floor >= 0),
    
    FOREIGN KEY (ClimateControlled) REFERENCES ClimateControl(ClimateControlled)
);

CREATE TABLE RentalContract (
    ID SERIAL PRIMARY KEY,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    MonthlyRate DECIMAL(10, 2) NOT NULL 
    Customer_ID INTEGER NOT NULL,
    Unit_ID INTEGER NOT NULL,
    
    CONSTRAINT CheckRentalContractMonthlyRateValue CHECK (MonthlyRate >= 0),
    CONSTRAINT CheckRentalContractEndDateValue CHECK (EndDate > StartDate),

    FOREIGN KEY (Customer_ID) REFERENCES Customer(ID),
    FOREIGN KEY (Unit_ID) REFERENCES StorageUnit(ID)
);

CREATE TABLE Payment (
    ID SERIAL PRIMARY KEY,
    PaymentDate DATE NOT NULL,
    Amount DECIMAL(10, 2) NOT NULL 
    Method VARCHAR(50) NOT NULL,
    Contract_ID INTEGER NOT NULL,

    CONSTRAINT CheckPaymentAmountValue CHECK (Amount >= 0),

    FOREIGN KEY (Contract_ID) REFERENCES RentalContract(ID)
);
