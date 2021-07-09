# DeepMetis: Augmenting a Deep Learning Test Set to Increase its Mutation Score

## General Information ##
This repository contains the source code and the data of the paper "DeepMetis: Augmenting a Deep Learning Test Set to Increase its Mutation Score" by V. Riccio, N. Humbatova, G. Jahangirova, and P. Tonella, to be published in the Proceedings of the 36th IEEE/ACM International Conference on Automated Software Engineering (ASE 2021).

## Repository Structure ##
The package is structured as follows:

* [__DeepMetis-MNIST__](./DeepMetis-MNIST) contains the DeepMetis tool adapted to the handwritten digit classification case study and the instructions on how to use it;
* [__DeepMetis-UE__](./DeepMetis-UE) contains the DeepMetis tool adapted to the eye gaze prediction case study and the instructions on how to use it;
* [__experiments__](./experiments) contains the raw experimental data and the scripts to obtain the results reported in the paper;
* [__installation_guide__](./INSTALL.md) contains a quick installation guide of the tool.
* [__preprint__](./deepmetis_paper.pdf) is the preprint version of our paper describing DeepMetis.

_Note:_ each sub-package contains further specific instructions.

## License ##
The software we developed is distributed under MIT license. See the [license](./LICENSE) file.

## Contacts

For any related question, please contact its authors: 
* Vincenzo Riccio ([vincenzo.riccio@usi.ch](mailto:vincenzo.riccio@usi.ch))
* Nargiz Humbatova ([nargiz.humbatova@usi.ch](mailto:nargiz.humbatova@usi.ch))
* Gunel Jahangirova ([gunel.jahangirova@usi.ch](mailto:gunel.jahangirova@usi.ch))
* Paolo Tonella ([paolo.tonella@usi.ch](mailto:paolo.tonella@usi.ch)).

## Reference

If our work helps your research, please cite DeepMetis in your publications. 
Here is an example BibTeX entry:

```
@inproceedings{DeepMetis_ASE_2021,
	title= {DeepMetis: Augmenting a Deep Learning Test Set to Increase its Mutation Score},
	author= {Vincenzo Riccio and Nargiz Humbatova and Gunel Jahangirova and Paolo Tonella},
	booktitle= {Proceedings of the 36th IEEE/ACM International Conference on Automated Software Engineering},
	series= {ASE '21},
	publisher= {IEEE/ACM},
	year= {2021}
}
```
