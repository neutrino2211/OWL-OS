console.log("Requiring Mem")
var mem = require("./native/build/Release/mem_ctl");
var cluster = require("cluster");

console.log("Mem required successfully")
console.log("Storing value of Hello")
let h = mem.Hello()
console.log("Hello value stored")
var bus = new mem.Bus();
async function init() {
    console.log(bus.getModuleId("test"))
    console.log("Creating threads")
    // await simult();
    // await r();
    console.log("---------------------------------------")
    var testID = bus.getModuleId("test")
    mem.new_thread();
    try {
        setTimeout(function(){
            console.log(testID);
            bus.read(testID,function(id,ptr,isptr){
                console.log("Callback!!!!!!!!!!!!!!!!!!!!")
                console.log("ID : "+id);
                console.log("PTR : "+ptr);
                console.log("ISPTR : "+isptr);
            })
        },2000)
    } catch (e) {
        console.log(e)
    }
    console.log("Threads created")
}

async function r(){
    mem.new_thread();
    return
}

async function simult(){
    console.log("---------------------------------------")
        bus.read(bus.getModuleId("test"),function(id,ptr,isptr){
            console.log("ID : "+id);
            console.log("PTR : "+ptr);
            console.log("ISPTR : "+isptr);
        })
        return;
}
init()
// simult();