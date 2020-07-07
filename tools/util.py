
import collections
import copy




class Tree(collections.defaultdict):
    """Tree data structure
    This class models a tree data structure that is mainly used to store
    experiment parameters and results in a hierarchical form that makes it
    easier to search and filter data in them.
    """

    def __init__(self, data=None, **attr):
        """Constructor
        Parameters
        ----------
        data : input data
            Data from which building a tree. Types supported are Tree objects
            and dicts (or object that can be cast to trees), even nested.
        attr : additional keyworded attributes. Attributes can be trees of leaf
            values. If they're dictionaries, they will be converted to trees
        """
        if data is None:
            data = {}
        elif not isinstance(data, Tree):
            # If data is not a Tree try to cast to dict and iteratively recurse
            # it to convert each node to a tree
            data = dict(data)
            for k in data:
                if not isinstance(data[k], Tree) and isinstance(data[k], dict):
                    data[k] = Tree(data[k])
        # Add processed data to the tree
        super(Tree, self).__init__(Tree, data)
        if attr:
            self.update(attr)

    def __iter__(self, root=[]):
        it = collections.deque()
        for k_child, v_child in self.items():
            base = copy.copy(root)
            base.append(k_child)
            if isinstance(v_child, Tree):
                it.extend(v_child.__iter__(base))
            else:
                it.append((tuple(base), v_child))
        return iter(it)

    def __setitem__(self, k, v):
        if not isinstance(v, Tree) and isinstance(v, dict):
            v = Tree(v)
        super(Tree, self).__setitem__(k, v)

    def __reduce__(self):
        # This code is needed to fix an issue occurring while pickling.
        # Further info here:
        # http://stackoverflow.com/questions/3855428/how-to-pickle-and-unpickle-instances-of-a-class-that-inherits-from-defaultdict
        t = collections.defaultdict.__reduce__(self)
        return (t[0], ()) + t[2:]

    def __str__(self, dictonly=False):
        """Return a string representation of the tree
        Parameters
        ----------
        dictonly : bool, optional
            If True, just return a representation of a corresponding dictionary
        Returns
        -------
        tree : str
            A string representation of the tree
        """
        return "Tree({})".format(self.dict())

    @property
    def empty(self):
        """Return True if the tree is empty, False otherwise"""
        return len(self) == 0

    def update(self, e):
        """Update tree from e, similarly to dict.update
        Parameters
        ----------
        e : Tree
            The tree to update from
        """
        if not isinstance(e, Tree):
            e = Tree(e)
        super(Tree, self).update(e)

    def paths(self):
        """Return a dictionary mapping all paths to final (non-tree) values
        and the values.
        Returns
        -------
        paths : dict
            Path-value mapping
        """
        return dict(iter(self))

    def getval(self, path):
        """Get the value at a specific path, None if not there
        Parameters
        ----------
        path : iterable
            Path to the desired value
        Returns
        -------
        val : any type
            The value at the given path
        """
        tree = self
        for i in path:
            if isinstance(tree, Tree) and i in tree:
                tree = tree[i]
            else:
                return None
        return None if isinstance(tree, Tree) and tree.empty else tree

    def setval(self, path, val):
        """Set a value at a specific path
        Parameters
        ----------
        path : iterable
            Path to the value
        val : any type
            The value to set at the given path
        """
        tree = self
        for i in path[:-1]:
            if not isinstance(tree[i], Tree):
                tree[i] = Tree()
            tree = tree[i]
        tree[path[-1]] = val

    def dict(self, str_keys=False):
        """Convert the tree in nested dictionaries
        Parameters
        ----------
        str_key : bool, optional
            Convert keys to string. This is useful for example to dump a dict
            into a JSON object that requires keys to be strings
        Returns
        -------
        d : dict
            A nested dict representation of the tree
        """
        d = {}
        for k, v in self.items():
            k = str(k) if str_keys else k
            v = v.dict() if isinstance(v, Tree) else v
            d[k] = v
        return d

    def match(self, condition):
        """Check if the tree matches a given condition.
        The condition is another tree. This method iterates to all the values
        of the condition and verify that all values of the condition tree are
        present in this tree and have the same value.
        Note that the operation is not symmetric i.e.
        self.match(condition) != condition.match(self). In fact, this method
        return True if this tree has values not present in the condition tree
        while it would return False if the condition has values not present
        in this tree.
        Parameters
        ----------
        condition : Tree
            The condition to check
        Returns
        -------
        match : bool
            True if the tree matches the condition, False otherwise.
        """
        condition = Tree(condition)
        return all(self.getval(path) == val for path, val in condition.paths().items())