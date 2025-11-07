//Functions enumAllClasses and enumMethods provided by

/** * raptor_frida_android_*.js - Frida snippets for Android
 * Copyright (c) 2017 Marco Ivaldi <raptor@0xdeadbeef.info>
*/

//https://github.com/0xdea/frida-scripts/blob/master/android-snippets/raptor_frida_android_findClass1.js



function enumAllClasses()
{
	var allClasses = [];
	var classes = Java.enumerateLoadedClassesSync();

	classes.forEach(function(aClass) {
		try {
			var className = aClass.match(/[L](.*);/)[1].replace(/\//g, ".");
		}
		catch(err) {return;} // Avoid TypeError: cannot read property 1 of null
		allClasses.push(className);
	});

	return allClasses;
}


function enumMethods(targetClass)
{
	var hook = Java.use(targetClass);
	var ownMethods = hook.class.getDeclaredMethods();
	hook.$dispose();

	return ownMethods;
}

console.log("Starting class dumping, this should take approsimately 25 seconds")
setTimeout(function() { // Avoid java.lang.ClassNotFoundException
	Java.perform(function() {
		var allClasses = enumAllClasses();
		var errors = 0;
		var class_successes = 0;
		var methods_successes = 0;


		allClasses.forEach(function(s) { 
			try{
				console.log("------------------------------")
				console.log("CLASS "+s)
				var x = enumMethods(s)
				console.log("METHODS")
				x.forEach(function(newMethod){
					console.log(newMethod)
					methods_successes++;
				})
				class_successes++;
			}
			catch{
				errors++;
			}
		});
		
		console.log("Dumped " + class_successes + " classes successfully" )
		console.log("Dumped " + methods_successes + " methods successfully")
		console.log("Failed to dump " + errors + " classes")
	});
}, 10000);