package com.SwapTreasure.app;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.servlet.ModelAndView;

@Controller
public class ArtifactsController {
	@Autowired
	AdRepo repo;
	@RequestMapping("/")
	public String placeAdd() {
		return "Homepage.jsp";
	}
	
	@RequestMapping("/placeAd")
	public String addAlien(Artifacts ad) {
		repo.save(ad);
		return "PlaceAd.jsp";
	}
	
	@RequestMapping("/getAdbyid")
	public ModelAndView getAd(@RequestParam int aid) {
		ModelAndView mv = new ModelAndView("DisplayAd.jsp");  //follow this
		Artifacts ad = repo.findById(aid).orElse(new Artifacts());
		mv.addObject(ad);
		return mv;
	}
	
	
	
	
	@RequestMapping("/tresures1")
	@ResponseBody
	public List<Artifacts> getTresures() {	
		return repo.findAll();
		
	}
	
	@RequestMapping("/getAllAd")
	public ModelAndView getAllAd() {
		ModelAndView mv = new ModelAndView("Treasures.jsp");  //follow this
		ArrayList<Artifacts> ad = (ArrayList<Artifacts>) repo.findAll();
		mv.addObject(ad);
		return mv;
	}
	
	@RequestMapping("/tresures")
	public ModelAndView getAd1() {
		ModelAndView mv = new ModelAndView("Treasures.jsp");  //follow this
		Artifacts ad = repo.findById(213).orElse(new Artifacts());
		mv.addObject(ad);
		return mv;
	}
	
	
//	@RequestMapping("/tresures/{aid}")
//	@ResponseBody
//	public Optional<Ad> getArtifact(@PathVariable("aid")int aid)
//	{
//		return repo.findById(aid);
//	}
	
	
//	@PostMapping("/tresures")
//	public Ad getTresures2(@RequestBody Ad ad) {	
//		repo.save(ad);
//		return ad;
//	}
//	

	//Delete
	@DeleteMapping("/deltresures/{aid}")
	@ResponseBody
	public Artifacts deleteArtifact()
	{
		Artifacts ad=repo.getOne(156);
		repo.delete(ad);
		return ad;
	}
	
	
	
	//Save
	@PutMapping(path="/tresures",consumes= {"application/json"})
	public Artifacts updateArtifact(@RequestBody Artifacts ad)
	{
		repo.save(ad);
		return ad;
	}
}

