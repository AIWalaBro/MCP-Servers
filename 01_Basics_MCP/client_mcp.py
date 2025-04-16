import requests

def test_multiply(a,b):
    response = requests.post("http://127.0.0.1:8080/aiwalabro/mcp/multiply", json = {"a":a , "b":b})
    if response.status_code == 200 :
        print("multiplication mcp called succefully",response.json()["result"])
    else :
        print("there was an issue with the mcp call")

if __name__ == "__main__":
    test_multiply(9,10)
