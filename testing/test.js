import Replicate from "replicate";
// Make sure REPLICATE_API_TOKEN is set to your Hack Club AI API key
const replicate = new Replicate({ baseUrl: "https://ai.hackclub.com/proxy/v1/replicate" });

const input = {
    voice: "William (Whispering)",
    prompt: "Poppin' bottles in the ice, like a blizzard.\nWhen we drink, we do it right, gettin' slizzered\nSippin' sizzurp in my ride (in my ride) like Three 6.\nNow I'm feelin' so fly like a G 6"
};

const output = await replicate.run("resemble-ai/chatterbox-pro", { input });

// To access the file URL:
console.log(output.url());