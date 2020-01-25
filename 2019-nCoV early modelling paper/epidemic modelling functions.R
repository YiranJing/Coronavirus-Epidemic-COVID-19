
	# Jonathan Read, Jessica Bridgen, Chris Jewell, Jan 2020
	# Lancaster University
	# email: jonathan.read@lancaster.ac.uk 

	

	import.matrix = function(filename, replace.NA.w.zero=FALSE) {
		#imports from file with row names as column 1.
		tmp = read.csv(filename, stringsAsFactors=FALSE)
		n = ncol(tmp)-1
		M = data.matrix(tmp[,1+(1:n)])
		rownames(M) = tmp[,1]
		if (replace.NA.w.zero) {
			M[is.na(M)] = 0
		}
		return(M)
	}

	# transmission model functions
	epidemic.sim = function( beta_1, gamma, alpha, phi, I0W, t.max=19, 
		K1, K2, t.K.switch=NA, K1x=NULL ) {
		# presumed epidemic start
		I0 = numeric(m)
		I0[which(city.seq=="Wuhan")] = I0W
		I = I0
		S = N - I
		E = 0
		R = 0

		# number of confirmed cases (R), China
		res_China = matrix(0,nrow=m,ncol=t.max+1)
		rownames(res_China) = city.seq
		res_China[,1] = R
		
		# number of imported infections, World
		res_World = matrix(0,nrow=w,ncol=t.max+1)
		rownames(res_World) = country.seq
		
		# number of new (not existing) infections, China
		I_China = matrix(0,nrow=m,ncol=t.max+1)
		rownames(I_China) = city.seq 
		# number of current infections, China
		Icurr_China = matrix(0,nrow=m,ncol=t.max+1)
		rownames(Icurr_China) = city.seq 
		
		for (k in 1:t.max) {
			if (!is.na(t.K.switch) & k>=t.K.switch) {
				I_hat = S*( beta_1*(I/N) + beta_1*t(K1x/N)%*%(I/N) ) 				
			} else {
				I_hat = S*( beta_1*(I/N) + beta_1*t(K1/N)%*%(I/N) ) 
			}
			S = S - I_hat
			E = E + I_hat - alpha*E
			I = I + alpha*E - gamma*I
			R = R + gamma*I
			res_China[,k+1] = gamma*I
			res_World[,k+1] = t(K2/N)%*%(I)
			I_China[,k+1] = I_hat
			Icurr_China[,k+1] = I
		}
		return( 
			list( 
				res_China=res_China, 
				res_World=res_World, 
				I_China=I_China,
				Icurr_China=Icurr_China
			) 
		)
	}

	
	# likelihood functions
		invlogit = function(x) {
			expx = exp(x)
			expx /(1+expx)
		}
		logLikelihood = function( par, obs, alpha, t.max, K1, K2 ) {
			beta_1 =   exp(par[1]) # within-city transmission rate
			gamma =    exp(par[2]) # recovery rate
			phi = invlogit(par[3]) # ascertainment rate in Wuhan
			I0W =      exp(par[4]) # intiial infected at day 0 (1 Jan 2020)
			#alpha =    exp(par[5]) # incubation transition rate
			
			sim = epidemic.sim(beta_1, gamma, alpha, phi, I0W, t.max, K1, K2)

			#print( lapply(obs, dim) )
			#print( lapply(sim, dim) )
			print( paste( beta_1, gamma, phi, I0W ) )
			#browser()
			
			# China
			sim$res_China[151,] = phi*sim$res_China[151,] # wuhan
			china = dpois(obs$data_China[,1:(t.max+1)], sim$res_China, log=T)
			# World
			sim$res_World[151,] = phi*sim$res_World[151,] # wuhan
			world = dpois(obs$data_World[,1:(t.max+1)], sim$res_World, log=T)
			
			sum(china) + sum(world)
		}
			


	make.param = function( hess ) {
		param = data.frame(
			par=c("beta_1","gamma","phi","I0W"),
			estim=hess$par,
			se=sqrt( (1/diag(-hess$hessian)) )
		)
		param$value=c( 
				exp(param$estim[1]),
				exp(param$estim[2]),
				invlogit(param$estim[3]),
				exp(param$estim[4])
			)
		param$ci.lo=c( 
				exp(param$estim[1]-param$se[1]),
				exp(param$estim[2]-param$se[2]),
				invlogit(param$estim[3]-param$se[3]),
				exp(param$estim[4]-param$se[4])
			)
		param$ci.hi=c( 
				exp(param$estim[1]+param$se[1]),
				exp(param$estim[2]+param$se[2]),
				invlogit(param$estim[3]+param$se[3]),
				exp(param$estim[4]+param$se[4])
			)
		print( param )
		return( param )
	}


	
	get.R0.lims = function(param) {
		c( param$value[1]/param$value[2],
		   param$ci.lo[1]/param$ci.hi[2],
		   param$ci.hi[1]/param$ci.lo[2]
		 )
	}
	
	print.R0 = function(param) {
		R0 = get.R0.lims( param )
		paste0( 
			"R0: ",
			round( R0[1],2 ),
			" (",
			round( R0[2],2 ),
			" - ",
			round( R0[3],2 ),
			")"
		)
	}

	get.InfP.lims = function(param) {
		c( 1/param$value[2],
		   1/param$ci.hi[2],
		   1/param$ci.lo[2]
		)
	}
	
	print.InfP = function(param) {
		InfP = get.InfP.lims(param)
		paste0( 
			"InfP: ",
			round( InfP[1],2 ),
			" (",
			round( InfP[1],2 ),
			" - ",
			round( InfP[1],2 ),
			")"
		)
	}

	plot.alpha.sensitivity = function( hess, hess.alpha.lo, hess.alpha.hi ) {
		param = make.param( hess )
		param.alpha.lo = make.param( hess.alpha.lo )
		param.alpha.hi = make.param( hess.alpha.hi )
		R0 = get.R0.lims(param)
		R0.alpha.lo = get.R0.lims(param.alpha.lo)
		R0.alpha.hi = get.R0.lims(param.alpha.hi)
		InfP = get.InfP.lims(param)
		InfP.alpha.lo = get.InfP.lims(param.alpha.lo)
		InfP.alpha.hi = get.InfP.lims(param.alpha.hi)
			col.seq = c("darkolivegreen1","darkorange","darkolivegreen3")
			par( mfrow=c(1,5), mar=c(5,5,1,1), cex.lab=1.5, yaxs="r" )
			# R0
				ymax = max(c(R0.alpha.lo[3],R0[3],R0.alpha.hi[3]))
				plot( c(0.5,3.5), c(0,ymax), type="n",
					xlab=expression(1/alpha), ylab=expression(R[0]), axes=FALSE
				)
				axis(side=1,at=1:3, labels=c("3.6","4.0","4.4"))
				axis(side=2)
				rect( 0.6, R0.alpha.lo[2], 1.4, R0.alpha.lo[3], col=col.seq[1] )
				rect( 1.6, R0[2], 2.4, R0[3], col=col.seq[2] )
				rect( 2.6, R0.alpha.hi[2], 3.4, R0.alpha.hi[3], col=col.seq[3] )
				points( 1:3, c(R0.alpha.lo[1],R0[1],R0.alpha.hi[1]), pch=16 )
				abline( h=1, lty=2 )
			# beta_1
				ymin = min( c(param.alpha.lo$ci.lo[1],param$ci.lo[1],param.alpha.hi$ci.lo[1]) )
				ymax = max( c(param.alpha.lo$ci.hi[1],param$ci.hi[1],param.alpha.hi$ci.hi[1]) )
				plot( c(0.5,3.5), c(ymin,ymax), type="n",
					xlab=expression(1/alpha), ylab=expression(beta[1]), axes=FALSE
				)
				axis(side=1,at=1:3, labels=c("3.6","4.0","4.4"))
				axis(side=2)
				rect( 0.6, param.alpha.lo$ci.lo[1], 1.4, param.alpha.lo$ci.hi[1], col=col.seq[1] )
				rect( 1.6, param$ci.lo[1], 2.4, param$ci.hi[1], col=col.seq[2] )
				rect( 2.6, param.alpha.hi$ci.lo[1], 3.4, param.alpha.hi$ci.hi[1], col=col.seq[3] )
				points( 1:3, c(param.alpha.lo$value[1],param$value[1],param.alpha.hi$value[1]), pch=16 )
			# gamma
				ymin = min( c(param.alpha.lo$ci.lo[2],param$ci.lo[2],param.alpha.hi$ci.lo[2]) )
				ymax = max( c(param.alpha.lo$ci.hi[2],param$ci.hi[2],param.alpha.hi$ci.hi[2]) )
				plot( c(0.5,3.5), c(ymin,ymax), type="n",
					xlab=expression(1/alpha), ylab=expression(gamma), axes=FALSE
				)
				axis(side=1,at=1:3, labels=c("3.6","4.0","4.4"))
				axis(side=2)
				rect( 0.6, param.alpha.lo$ci.lo[2], 1.4, param.alpha.lo$ci.hi[2], col=col.seq[1] )
				rect( 1.6, param$ci.lo[2], 2.4, param$ci.hi[2], col=col.seq[2] )
				rect( 2.6, param.alpha.hi$ci.lo[2], 3.4, param.alpha.hi$ci.hi[2], col=col.seq[3] )
				points( 1:3, c(param.alpha.lo$value[2],param$value[2],param.alpha.hi$value[2]), pch=16 )
			# phi
				ymin = min( c(param.alpha.lo$ci.lo[3],param$ci.lo[3],param.alpha.hi$ci.lo[3]) )
				ymax = max( c(param.alpha.lo$ci.hi[3],param$ci.hi[3],param.alpha.hi$ci.hi[3]) )
				plot( c(0.5,3.5), c(ymin,ymax), type="n",
					xlab=expression(1/alpha), ylab=expression(phi), axes=FALSE
				)
				axis(side=1,at=1:3, labels=c("3.6","4.0","4.4"))
				axis(side=2)
				rect( 0.6, param.alpha.lo$ci.lo[3], 1.4, param.alpha.lo$ci.hi[3], col=col.seq[1] )
				rect( 1.6, param$ci.lo[3], 2.4, param$ci.hi[3], col=col.seq[2] )
				rect( 2.6, param.alpha.hi$ci.lo[3], 3.4, param.alpha.hi$ci.hi[3], col=col.seq[3] )
				points( 1:3, c(param.alpha.lo$value[3],param$value[3],param.alpha.hi$value[3]), pch=16 )
			# I0W
				ymin = min( c(param.alpha.lo$ci.lo[4],param$ci.lo[4],param.alpha.hi$ci.lo[4]) )
				ymax = max( c(param.alpha.lo$ci.hi[4],param$ci.hi[4],param.alpha.hi$ci.hi[4]) )
				plot( c(0.5,3.5), c(ymin,ymax), type="n",
					xlab=expression(1/alpha), ylab=expression(I[W](0)), axes=FALSE
				)
				axis(side=1,at=1:3, labels=c("3.6","4.0","4.4"))
				axis(side=2)
				rect( 0.6, param.alpha.lo$ci.lo[4], 1.4, param.alpha.lo$ci.hi[4], col=col.seq[1] )
				rect( 1.6, param$ci.lo[4], 2.4, param$ci.hi[4], col=col.seq[2] )
				rect( 2.6, param.alpha.hi$ci.lo[4], 3.4, param.alpha.hi$ci.hi[4], col=col.seq[3] )
				points( 1:3, c(param.alpha.lo$value[4],param$value[4],param.alpha.hi$value[4]), pch=16 )
	}
	
	
	get.mean.CI = function(x) {
		c( mean(x), quantile(x,probs=c(0.025,0.975)) )
	}

	
	tcol = function(colour,s=0.1) {
		# coverts colour (character) to transparent rgb hex code.
		f = as.numeric(col2rgb(colour))/255
		g = rgb( f[1], f[2], f[3], s )
		return( g )
	}

	get.ts = function(X, name) {
		i = which( rownames(X)==name )
		X[i,]
	}
	stack.x = function(x) {
		M = x[[1]]
		for (k in 2:length(x)) {
			M = rbind(M,x[[k]])
		}
		rownames(M) = NULL
		return(M)
	}
	
	plot.time.series = function( a, full.I_China, full.res_World, t.now, t.plus ) {
		# selected city time series
		#wuhan = apply( stack.x(lapply(full.I_China, FUN=get.ts, name="Wuhan")), MARGIN=2, FUN=get.mean.CI )
		wuhan = stack.x(lapply(full.I_China, FUN=get.ts, name="Wuhan"))
		wuhan_detect =stack.x(lapply(full.I_China, FUN=get.ts, name="Wuhan"))*phi
		
		beijing = stack.x( lapply( full.I_China, FUN=get.ts, name="Beijing"))
		chengdu = stack.x( lapply( full.I_China, FUN=get.ts, name="Chengdu"))
		guangzhou = stack.x( lapply( full.I_China, FUN=get.ts, name="Guangzhou"))
		shanghai = stack.x( lapply( full.I_China, FUN=get.ts, name="Shanghai"))
		shenzhen = stack.x( lapply( full.I_China, FUN=get.ts, name="Shenzhen"))
	
		thailand = stack.x(lapply(full.res_World, FUN=get.ts, name="Thailand"))
		japan = stack.x(lapply(full.res_World, FUN=get.ts, name="Japan"))
		skorea = stack.x(lapply(full.res_World, FUN=get.ts, name="Korea.Republic.of"))
		usa = stack.x(lapply(full.res_World, FUN=get.ts, name="USA"))
		taiwan = stack.x(lapply(full.res_World, FUN=get.ts, name="Chinese.Taipei"))
		uk = stack.x(lapply(full.res_World, FUN=get.ts, name="United.Kingdom"))
	
		par( mfrow=c(1,3), mar=c(5,5,2,1), cex.axis=0.9, las=1 )
		t.seq = 1+(t.now:(t.now+t.plus))
		x.seq = date.seq[t.seq]
		# A Wuhan
			plot( 
				range(x.seq), 
				c(0,200),
				type="n", log="", 
				xlab="", ylab="New infections, 1000s per day"
			) 
			s = 0.01
			for (repl in 1:repl.max) {
				lines( x.seq, wuhan[repl,t.seq]/1000,        col=tcol("black" ,s) )
				lines( x.seq, wuhan_detect[repl,t.seq]/1000, col=tcol("salmon",s) )
			}
			s = 1
				lines( x.seq, a$I_China[151,t.seq]/1000,     col=tcol("black" ,s) )
				lines( x.seq, phi*a$I_China[151,t.seq]/1000, col=tcol("salmon",s) )
			legend( 
				"topleft", 
				bty="n", 
				legend=c("Wuhan - all","Wuhan - detected"), 
				lty=1, 
				col=c("black","salmon"), 
				cex=1
			)
			mtext(side=3, "A", adj=0, font=2, cex=1.5 )
		# B China cities
			plot( 
				range(x.seq), 
				c(0,1000),
				type="n", log="", 
				xlab="", ylab="New infections, per day"
			) 
			s = 0.01
			for (repl in 1:repl.max) {
				lines( x.seq,   beijing[repl,t.seq], col=tcol("red" ,s) )
				lines( x.seq,   chengdu[repl,t.seq], col=tcol("blue" ,s) )
				lines( x.seq, guangzhou[repl,t.seq], col=tcol("goldenrod" ,s) )
				lines( x.seq,  shanghai[repl,t.seq], col=tcol("forestgreen" ,s) )
				lines( x.seq,  shenzhen[repl,t.seq], col=tcol("purple" ,s) )
			}
			s = 1
				lines( x.seq, a$I_China[which(city.seq=="Beijing"),t.seq], col=tcol("red" ,s) )
				lines( x.seq, a$I_China[which(city.seq=="Chengdu"),t.seq], col=tcol("blue" ,s) )
				lines( x.seq, a$I_China[which(city.seq=="Guangzhou"),t.seq], col=tcol("goldenrod" ,s) )
				lines( x.seq, a$I_China[which(city.seq=="Shanghai"),t.seq], col=tcol("forestgreen" ,s) )
				lines( x.seq, a$I_China[which(city.seq=="Shenzhen"),t.seq], col=tcol("purple" ,s) )
			legend( 
				"topleft", 
				bty="n", 
				legend=c("Beijing","Chengdu","Guangzhou","Shanghai","Shenzen"), 
				lty=1, 
				col=c("red","blue","goldenrod","forestgreen","purple"), 
				cex=1
			)
			mtext(side=3, "B", adj=0, font=2, cex=1.5 )
		# C Other countries
			plot( 
				range(x.seq), 
				c(0,20),
				type="n", log="", 
				xlab="", ylab="Importations, per day"
			) 
			s = 0.01
			for (repl in 1:repl.max) {
				lines( x.seq,   thailand[repl,t.seq], col=tcol("red" ,s) )
				lines( x.seq,   japan[repl,t.seq], col=tcol("blue" ,s) )
				lines( x.seq,   skorea[repl,t.seq], col=tcol("goldenrod" ,s) )
				lines( x.seq,   usa[repl,t.seq], col=tcol("forestgreen" ,s) )
				lines( x.seq,   taiwan[repl,t.seq], col=tcol("purple" ,s) )
				lines( x.seq,   uk[repl,t.seq], col=tcol("salmon" ,s) )
			}
			s = 1
				lines( x.seq, a$res_World[which(country.seq=="Thailand"),t.seq],          col=tcol("red" ,s) )
				lines( x.seq, a$res_World[which(country.seq=="Japan"),t.seq],             col=tcol("blue" ,s) )
				lines( x.seq, a$res_World[which(country.seq=="Korea.Republic.of"),t.seq], col=tcol("goldenrod" ,s) )
				lines( x.seq, a$res_World[which(country.seq=="USA"),t.seq],               col=tcol("forestgreen" ,s) )
				lines( x.seq, a$res_World[which(country.seq=="Chinese.Taipei"),t.seq],    col=tcol("purple" ,s) )
				lines( x.seq, a$res_World[which(country.seq=="United.Kingdom"),t.seq],    col=tcol("salmon" ,s) )
			legend( 
				"topleft", 
				bty="n", 
				legend=c("Thailand","Japan","South Korea","USA","Taiwan","UK"), 
				lty=1, 
				col=c("black","red","blue","goldenrod","forestgreen","purple","salmon"), 
				cex=1
			)
			mtext(side=3, "C", adj=0, font=2, cex=1.5 )
		}
	
	
	
	plot.travel.restrictions = function( K1, t.now, t.plus ) {
		t.seq = 1+(t.now:(t.now+t.plus))
		
	
		i = 151 #wuhan
		K1.50 = K1
		K1.50[i,] = K1[i,]*0.5
		K1.50[,i] = K1[,i]*0.5
		K1.80 = K1
		K1.80[i,] = K1[i,]*0.2
		K1.80[,i] = K1[,i]*0.2
		K1.90 = K1
		K1.90[i,] = K1[i,]*0.1
		K1.90[,i] = K1[,i]*0.1
		K1.95 = K1
		K1.95[i,] = K1[i,]*0.05
		K1.95[,i] = K1[,i]*0.05
		K1.99 = K1
		K1.99[i,] = K1[i,]*0.01
		K1.99[,i] = K1[,i]*0.01
		K1.100 = K1
		K1.100[i,] = K1[i,]*0.0
		K1.100[,i] = K1[,i]*0.0

		a = epidemic.sim( 
			beta_1=param$value[1], 
			gamma=param$value[2], 
			alpha=1/4, 
			phi=param$value[3], 
			I0W=param$value[4],
			t.max=t.now+t.plus,
			K1, K2
		)
		a.50 = epidemic.sim( 
			beta_1=param$value[1], 
			gamma=param$value[2], 
			alpha=1/4, 
			phi=param$value[3], 
			I0W=param$value[4],
			t.max=t.now+t.plus,
			K1, K2,
			t.K.switch=22, # 23 Jan 2020
			K1x=K1.50
		)
		a.80 = epidemic.sim( 
			beta_1=param$value[1], 
			gamma=param$value[2], 
			alpha=1/4, 
			phi=param$value[3], 
			I0W=param$value[4],
			t.max=t.now+t.plus,
			K1, K2,
			t.K.switch=22, # 23 Jan 2020
			K1x=K1.80
		)
		a.90 = epidemic.sim( 
			beta_1=param$value[1], 
			gamma=param$value[2], 
			alpha=1/4, 
			phi=param$value[3], 
			I0W=param$value[4],
			t.max=t.now+t.plus,
			K1, K2,
			t.K.switch=22, # 23 Jan 2020
			K1x=K1.90
		)
		a.95 = epidemic.sim( 
			beta_1=param$value[1], 
			gamma=param$value[2], 
			alpha=1/4, 
			phi=param$value[3], 
			I0W=param$value[4],
			t.max=t.now+t.plus,
			K1, K2,
			t.K.switch=22, # 23 Jan 2020
			K1x=K1.95
		)
		a.99 = epidemic.sim( 
			beta_1=param$value[1], 
			gamma=param$value[2], 
			alpha=1/4, 
			phi=param$value[3], 
			I0W=param$value[4],
			t.max=t.now+t.plus,
			K1, K2,
			t.K.switch=22, # 23 Jan 2020
			K1x=K1.99
		)
		a.100 = epidemic.sim( 
			beta_1=param$value[1], 
			gamma=param$value[2], 
			alpha=1/4, 
			phi=param$value[3], 
			I0W=param$value[4],
			t.max=t.now+t.plus,
			K1, K2,
			t.K.switch=22, # 23 Jan 2020
			K1x=K1.100
		)
		# find total number of infections over time outside of china, for each intervention
		i = which(city.seq!="Wuhan")
		x.50 = colSums( t(apply( a.50$I_China[i,t.seq], MARGIN=1, FUN=cumsum )) )
		x.80 = colSums( t(apply( a.80$I_China[i,t.seq], MARGIN=1, FUN=cumsum )) )
		x.90 = colSums( t(apply( a.90$I_China[i,t.seq], MARGIN=1, FUN=cumsum )) )
		x.95 = colSums( t(apply( a.95$I_China[i,t.seq], MARGIN=1, FUN=cumsum )) )
		x.99 = colSums( t(apply( a.99$I_China[i,t.seq], MARGIN=1, FUN=cumsum )) )
		x.100 = colSums( t(apply( a.100$I_China[i,t.seq], MARGIN=1, FUN=cumsum )) )
		# find total number of infections over time outside of china, with no intervention
		y = colSums( t(apply(    a$I_China[i,t.seq], MARGIN=1, FUN=cumsum )) )
		
		par( mar=c(5,5,2,1), cex.axis=0.8, las=1 )
		x.seq = date.seq[t.seq]
		# all other cities
		col.seq = colorRampPalette(c("skyblue","salmon"))(5)
		plot( 
			range(x.seq), 
			c(65,100), 
			type="n", 
			xlab="", ylab="% epidemic reduction" 
		)
		lines( x.seq, 100*(x.50/y), col=col.seq[1] ) 
		lines( x.seq, 100*(x.80/y), col=col.seq[2] ) 
		lines( x.seq, 100*(x.90/y), col=col.seq[3] ) 
		lines( x.seq, 100*(x.95/y), col=col.seq[4] )  
		lines( x.seq, 100*(x.99/y), col=col.seq[5] ) 
		legend("bottomleft",
			bty="n",
			legend=c("50%","80%","90%","95%","99%"),
			lty=1, col=col.seq,
			title="% reduction in travel"
		)
		# print output
		print( "% reduction in infections in rest of China" )
		print( paste( "50%:", tail(round(100*(1-x.50/y),1))[1] ) )
		print( paste( "80%:", tail(round(100*(1-x.80/y),1))[1] ) )
		print( paste( "90%:", tail(round(100*(1-x.90/y),1))[1] ) )
		print( paste( "95%:", tail(round(100*(1-x.95/y),1))[1] ) ) 
		print( paste( "99%:", tail(round(100*(1-x.99/y),1))[1] ) )
		print( paste( "100%:", tail(round(100*(1-x.100/y),1))[1] ) )
	}
		
