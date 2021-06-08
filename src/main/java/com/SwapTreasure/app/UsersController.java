package com.SwapTreasure.app;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller 
public class UsersController {
		@Autowired 
		RegRepo repo;
		
		
		@RequestMapping("/register")
		public String register(Users reg) {
			repo.save(reg);
			return "index.jsp";
		}
}
