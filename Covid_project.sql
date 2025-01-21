create database projects;

use projects;

SELECT * from coviddeaths;



-- Select Data that we are going to be starting with
Select Location, date, total_cases, new_cases, total_deaths, population
From CovidDeaths
Where continent is not null 
order by 1,2


-- Total Cases vs Total Deaths
-- Shows likelihood of dying if you contract covid in your country
Select Location, date, total_cases,total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
From CovidDeaths
where continent is not null 
order by 1,2

## FOCUS ON UNITED STATES:
Select Location, date, total_cases,total_deaths, (total_deaths/total_cases)*100 as DeathPercentage
From CovidDeaths
Where location like '%states%'
and continent is not null 
order by 1,2


#Looking at the total_cases vs population
#Shows what percentage of pupulation got covid

Select Location, date, total_cases,population, (total_cases/population)*100 as Covid_Percentage
From CovidDeaths
Where continent is not null 
order by 1,2

#FOCUS on USA
Select Location, date, total_cases,population, (total_cases/population)*100 as Covid_Percentage
From CovidDeaths
Where Location = "United States" and continent is not null 
order by 1,2


#Looking at countries with highest infection rates:
#WRONG
Select Location, total_cases,population, (total_cases/population)*100 as infection_rate
From CovidDeaths

order by infection_rate DESC


#RIGHT
Select Location, max(total_cases) as highestInfectionCount ,population, MAX((total_cases/population)*100) as infection_rate
From CovidDeaths
Group by Location, Population
order by infection_rate desc


# Countries with Highest Death Count per Population
#######################################################################

select continent,  sum(new_deaths)
from coviddeaths
where continent!=''
group by continent;

# NOW LETS DO GLOBAL NUMBERS
#The problem here is with the cast statement, dont use it
#With sum we do the sum of all cases, and then we make the death percentage(We dont use max in this case)

#TOTAL
Select SUM(new_cases) as total_cases, SUM(new_deaths) as total_deaths, SUM(new_deaths)/SUM(New_Cases)*100 as DeathPercentage
From CovidDeaths
where continent !=''
#Group By date
order by 1,2 

#POR FECHA
Select date, SUM(new_cases) as total_cases, SUM(new_deaths) as total_deaths, SUM(new_deaths)/SUM(New_Cases)*100 as DeathPercentage
From CovidDeaths
where continent !=''
Group By date
order by 1,2 desc

####################################################################################################################3
#PASAMOS A UTILIZAR LA OTRA TABLA

SELECT * FROM covidvaccinations

#LETS JOIN THIS TWO TABLES TOGETHER ON DATE AND LOCATION
 
SELECT * FROM coviddeaths dea
JOIN covidvaccinations vac
ON dea.location = vac.location
AND dea.date = vac.date

#LOOKING AT TOTAL POPULATION
#(AMOUNT OF PEOPLE IN THE WORLD THAT HAVE BEEN VACCINATED)

-- TOTAL POPULATION VS VACCINATIONS
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
FROM coviddeaths dea JOIN covidvaccinations vac
ON dea.location = vac.location AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
ORDER BY 2,3

## CALCULANDO LA SUMA ACUMULATIVA:
##CODE EXPLANATION: 1. SUM(vac.new_vaccinations)
#Esto calcula una suma acumulativa (rolling sum) de la columna new_vaccinations de la tabla vac.
#2. OVER (...)
#El uso de OVER indica que la función SUM se está usando como una función de ventana en lugar de una función agregada tradicional.
#3. PARTITION BY dea.Location
#Esta cláusula divide los datos en grupos (o particiones) basados en la columna dea.Location. Cada partición corresponde a un país o ubicación.

Select dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations
, SUM(vac.new_vaccinations) OVER (Partition by dea.Location Order by dea.location, dea.Date) as RollingPeopleVaccinated
-- (RollingPeopleVaccinated/population)*100
From CovidDeaths dea
Join CovidVaccinations vac
	On dea.location = vac.location
	and dea.date = vac.date
where dea.continent is not null 
order by 2,3
