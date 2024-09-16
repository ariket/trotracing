using System.IO;
using System.Net.Http;
using Python.Runtime;  //NuGet pythonnet
using Newtonsoft.Json; //NuGet Newtonsoft.Json

namespace trotracing
{
    internal class Program
    {
        public static void PythonWebScraping()
        {
            string pythonScript = "webscraping";
            string pythonScript2 = "result";
            string pythonScriptPath = "..\\..\\..\\ATG";
            Runtime.PythonDLL = @"C:\Python312\python312.dll";
            PythonEngine.Initialize();
            var threadState = PythonEngine.BeginAllowThreads();

            using var gil = Py.GIL();
            try
            {
                dynamic sys = Py.Import("sys");
                sys.path.append(pythonScriptPath);
                dynamic pythonModule = Py.Import(pythonScript);
                dynamic pythonModule2 = Py.Import(pythonScript2);
            }
            finally
            {
                gil.Dispose();
                PythonEngine.EndAllowThreads(threadState);
                PythonEngine.Shutdown();
            }
        }

        public static async Task<bool> GetDataFromATG(string RaceType)
        {
            
            string apiUrl = "https://www.atg.se/services/racinginfo/v1/api/products/" + RaceType;

            using HttpClient client = new();
            try
            {
                HttpResponseMessage response = await client.GetAsync(apiUrl);

                if (response.IsSuccessStatusCode)
                {
                    string responseData = await response.Content.ReadAsStringAsync();
                    ATGData ATGData = JsonConvert.DeserializeObject<ATGData>(responseData)!;

                    if (ATGData != null)
                    {
                        if (ATGData.UpComing != null)
                        {
                            int i = 0;
                            foreach (var race in ATGData.UpComing)
                            {
                                if (i++ == 0)
                                    Console.WriteLine($"{race}, {race.Tracks![0]} \n");

                                return ATGData.SetNextRace();
                            }
                        }
                        else
                        {
                            Console.WriteLine("Hittade inget tävlingsdatum");
                        }
                    }
                    else
                    {
                        Console.WriteLine("Ingenting sparades från ATGs API");
                    }
                }
                else
                {
                    Console.WriteLine($"Misslyckades att ladda ner data. Status kod: {response.StatusCode}");
                }
            }
            catch (HttpRequestException e)
            {
                Console.WriteLine($"Felmeddelande: {e.Message}");
            }

            return false;
        }
    }

    public class ATGData
    {
        public string BetType { get; set; } = "V75";
        public required List<Event> UpComing { get; set; }

        public bool SetNextRace()
        {
            //controls that race is in sweden(Track Id < 50) otherwise no scraping possible 
            if (this.UpComing[0]?.Tracks?[0].Id > 50)
            {
                Console.WriteLine($"Loppet går inte i Sverige: {this.UpComing[0]?.Tracks?[0].Name}" +
                                  $"\nSkrapningen kommer därför inte att kunna genomföras");
                return false;
            }
            
            string path = "..\\..\\..\\ATG\\data\\nextRace.txt";
            string nextRace = $"{this.UpComing[0].Id.Remove(0, 4)[0..10]}/{this.BetType}/{this.UpComing[0]?.Tracks?[0].Name}/";
            if (this.BetType == "V86" && this.UpComing[0].Tracks?.Count == 2)
                try
                {
                    nextRace = $"{this.UpComing[0].Id.Remove(0, 4)[0..10]}/{this.BetType}/{this.UpComing[0]?.Tracks?[1].Name}-{this.UpComing[0]?.Tracks?[0].Name}/";
                }
                catch
                {
                }
                
 
            Console.WriteLine($"Omgång: {nextRace}");
            string[] AllTextLines = File.ReadAllLines(path);
            AllTextLines[0] = nextRace;
            File.WriteAllLines(path, AllTextLines);
            return true;
        }
    }

    public class Event
    {
        public string Id { get; set; } = "V75";
        public DateTime StartTime { get; set; }
        public List<Tracks>? Tracks { get; set; }
        public List<Races>? Races { get; set; }
        public override string ToString()
        {
            return "Tävlings ID: " + Id;
        }
    }

    public class Tracks
    {
        public int Id { get; set; }
        public string? Name { get; set; }
        public override string ToString()
        {
            return "Banans namn: " + Name + " och ID: " + Id;
        }
    }

    public class Races 
    {
        public string? Id { get; set; }
        public List<Starts>? Starts { get; set; }
    }

    public class Starts
    {
        public int Number { get; set; }
        public Horse? Horse { get; set; }
    }

    public class Horse
    {
        public string? Name { get; set; }
    }

}
